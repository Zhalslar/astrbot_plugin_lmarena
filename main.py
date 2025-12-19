from collections import defaultdict
from datetime import datetime

from astrbot.api import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, StarTools
from astrbot.core import AstrBotConfig
from astrbot.core.message.components import Image
from astrbot.core.platform.astr_message_event import AstrMessageEvent

from .bridge.server import FastAPIWrapper, LMArenaBridgeServer
from .file_bed import ImageServer
from .utils import normalize_server
from .workflow import Workflow


class LMArenaPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.conf = config
        # 创建数据目录
        self.plugin_data_dir = StarTools.get_data_dir("astrbot_plugin_lmarena")
        self.file_bed_dir = self.plugin_data_dir / "file_bed"
        self.file_bed_dir.mkdir(parents=True, exist_ok=True)
        self.file_save_dir = self.plugin_data_dir / "file_save"
        self.file_save_dir.mkdir(parents=True, exist_ok=True)

        self.bridge_server = None
        self.api = None
        self.image_server = None

        # 提示词字典
        self.prompt_map = {}
        self.prompt_map_keys = []
        self._lode_prompt_map()

    async def initialize(self):
        self.bridge_server_url = normalize_server(self.conf.get("bridge_server", {}))
        self.image_server_url = normalize_server(self.conf.get("image_server", {}))

        # 桥梁服务器(必须)
        if self.bridge_server_url and self.conf["bridge_server"].get("url"):
            logger.info(f"已启用外置桥梁：{self.bridge_server_url}")
        elif self.bridge_server_url:
            self.bridge_server = LMArenaBridgeServer(self.conf)
            self.api = FastAPIWrapper(self.bridge_server, self.conf)
            self.api.start()
        else:
            logger.error("桥梁服务器配置错误，未能启动")

        # 图床服务器(非必须)
        if self.image_server_url and self.conf["image_server"].get("url"):
            logger.info(f"已启用远程图床：{self.image_server_url}")
        elif self.image_server_url:
            self.image_server = ImageServer(self.conf, self.file_bed_dir)
            self.image_server.start()

        # 工作流
        if self.bridge_server_url:
            self.workflow = Workflow(
                self.conf, self.bridge_server_url, self.image_server_url
            )
        else:
            logger.error("工作流未启动：bridge_server_url缺失")

    def _lode_prompt_map(self):
        prompt_list = self.conf["prompt_list"].copy()
        for item in prompt_list:
            if ":" in item:
                key, value = item.split(":", 1)
                self.prompt_map[key.strip()] = value.strip()
        self.prompt_map_keys = list(self.prompt_map.keys())

    @filter.event_message_type(filter.EventMessageType.ALL, priority=3)
    async def on_lmarena(self, event: AstrMessageEvent):
        """(图片)bnn 描述词 | (图片)触发词"""
        if self.conf["prefix"] and not event.is_at_or_wake_command:
            return

        text = event.message_str
        cmd = text.split()[0].strip() if text else ""
        # 纯文本模式、图片+自定义提示词模式
        if cmd == self.conf["extra_prefix"]:
            text = text.removeprefix(cmd).strip()
        # 图片+预设提示词模式
        elif cmd and cmd in self.prompt_map_keys:
            text = self.prompt_map.get(cmd) or ""
        else:
            return
        images: list[bytes | str] = await self.workflow.get_images(event)
        chat_res = await self.workflow.fetch_content(
            text=text,
            images=images,
            model="default_model",
            retries=self.conf["retries"],
        )

        if isinstance(chat_res, bytes):
            yield event.chain_result([Image.fromBytes(chat_res)])
            if self.conf["save_image"]:
                save_path = (
                    self.file_save_dir
                    / f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                )
                with save_path.open("wb") as f:
                    f.write(chat_res)

        elif isinstance(chat_res, str):
            yield event.plain_result(chat_res)

        else:
            yield event.plain_result("生成失败")
        event.stop_event()

    @filter.command("lm捕获", alias={"lmc"})
    async def update_id(self, event: AstrMessageEvent):
        """捕获会话ID"""
        if not self.bridge_server:
            yield event.plain_result("无法操作, 当前用的不是内置LM桥梁")
            return
        yield event.plain_result("已发送捕获命令, 请在浏览器中刷新目标模型")
        result = await self.bridge_server.update_id(
            host=self.conf["bridge_server"]["host"],
            port=int(self.conf["bridge_server"]["port"]) + 1,
            timeout=20,
        )
        yield event.plain_result(result)

    @filter.command("lm模型", alias={"lmm"})
    async def lm_model(self, event: AstrMessageEvent):
        """查看 lmarena 网页上的可用模型"""
        if not self.bridge_server:
            yield event.plain_result("无法操作，当前用的不是内置 LM 桥梁")
            return

        # 原始字典
        model_dict: dict[str, dict] = self.bridge_server.get_model_dict()

        # 按 type 分组
        buckets = defaultdict(list)
        for model_name, info in model_dict.items():
            buckets[info["type"]].append(model_name)

        # 拼装输出
        paragraphs = []
        for tp in sorted(buckets):
            chunk = [f"【{tp}模型】"]
            chunk += [f"{idx}. {name}" for idx, name in enumerate(buckets[tp], start=1)]
            paragraphs.append("\n".join(chunk))
        yield event.plain_result("\n\n".join(paragraphs))

    @filter.command("lm添加", alias={"lma"})
    async def add_lm_prompt(self, event: AstrMessageEvent):
        """lm添加 触发词:描述词（触发词重复则覆盖）"""
        raw = event.message_str.removeprefix("lm添加").removeprefix("lma").strip()
        if ":" not in raw:
            yield event.plain_result(
                "格式错误，正确示例：\n姿势表:为这幅图创建一个姿势表，摆出各种姿势"
            )
            return

        key, new_value = map(str.strip, raw.split(":", 1))

        # 1. 先尝试覆盖
        for idx, item in enumerate(self.conf["prompt_list"]):
            if item.startswith(key + ":"):  # 触发词相同
                self.conf["prompt_list"][idx] = f"{key}:{new_value}"
                break
        else:
            # 2. 没找到就新增
            self.conf["prompt_list"].append(f"{key}:{new_value}")

        self.conf.save_config()
        self._lode_prompt_map()
        yield event.plain_result(f"已保存LM生图提示语:\n{key}:{new_value}")

    @filter.command("lm帮助", alias={"lmh"})
    async def help(self, event: AstrMessageEvent, keyword: str | None = None):
        """Lmarena帮助"""
        if not keyword:
            msg = "可用的生图提示词：\n"
            msg += "、".join(self.prompt_map.keys())
            yield event.plain_result(msg)
            return
        prompt = self.prompt_map.get(keyword)
        if not prompt:
            yield event.plain_result("未找到此提示词")
            return
        yield event.plain_result(f"{keyword}:\n{prompt}")

    async def terminate(self):
        await self.workflow.terminate()
        if self.api:
            self.api.stop()
        if self.image_server:
            self.image_server.stop()
