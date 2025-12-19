
<div align="center">

![:name](https://count.getloli.com/@astrbot_plugin_lmarena?name=astrbot_plugin_lmarena&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto)

# astrbot_plugin_lmarena

_✨ LMArena插件 ✨_  

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-4.0%2B-orange.svg)](https://github.com/Soulter/AstrBot)
[![GitHub](https://img.shields.io/badge/作者-Zhalslar-blue)](https://github.com/Zhalslar)
</div>

# 警告：竞技场逆向已死，本插件已成废案，作者不再维护

## 🤝 介绍

全面对接lmarena，调用模型进行生图、聊天。 本插件相对其他生图插件而言，最大优势为无限额度免费调用，且支持竞技场的所有模型，最大缺点为需要浏览器和油猴脚本。

## 📦 安装
  
### 1.安装本插件

- 直接在astrbot的插件市场搜索astrbot_plugin_lmarena，点击安装

### 2.安装油猴脚本

- **安装油猴脚本管理器**
    为你的浏览器安装 [Tampermonkey](https://www.tampermonkey.net/) 扩展。

- **安装本项目油猴脚本**
    1. 打开 Tampermonkey 扩展的管理面板。
    2. 点击“添加新脚本”或“Create a new script”。
    3. 打开 [`LMArenaApiBridge.js`](https://github.com/Zhalslar/astrbot_plugin_lmarena/blob/main/LMArenaApiBridge.js) 文件，将文件里的所有代码复制并粘贴到编辑器中。
    4. 确保有权限运行（谷歌浏览器示例）：浏览器设置 -> 管理拓展 -> 篡改猴 -> 详情 -> 允许运行用户脚本（打开）。

### 3.插件与油猴对接

- 从Astrbot插件市场安装本插件（手动下载也行），启动插件时日志会显示：[bridge.server:74]: WebSocket 端点: ws://127.0.0.1:5102/ws
- 访问竞技场[LMArena.ai](https://lmarena.ai/)，注册、登录账号。
- 刷新[LMArena.ai](https://lmarena.ai/)页面让油猴脚本检测，等到Astrbot日志显示：✅ 油猴脚本已成功连接 WebSocket。并且[LMArena.ai](https://lmarena.ai/)页面页面标题会以 ✅ 开头，说明插件与油猴脚本对接成功。如果一直没对接上，请检查你的浏览器是否已允许运行油猴的脚本。

### 4.捕获会话ID

- 在[竞技场](<https://lmarena.ai>)找到你想要的模型(比如nano_banana)，图片模型需点击聊天栏左下角的图片图标（image）才会在列表里显示，Direct_chat模式才可以选模型，battle模式靠猜。
- 选好模型后，对话一次，直至出现Retry按钮。
- 然后给bot发送命令 `lm捕获`或`lmc`激活油猴脚本的捕获模式。
- 点模型的重试（Retry）按钮，刷新目标模型从而捕获会话ID，然后就可以正常使用了

## ⌨️ 使用说明

### 配置

请前往插件配置面板查看

### 命令表

|     命令      |                    说明                    |
|:-------------:|:-----------------------------------------------:|
| `(引用图片)/一段描述词`  | 将图片引用的图片按照描述词进行处理  |
| `lm捕获` or `lmc`  | 发送命令激活油猴脚本的捕获模式, 然后请在浏览器中刷新目标模型从而捕获会话ID    |
| `lm刷新` or `lmr` | 刷新lmarena网页    |
| `lm添加 xxx:xxx` or `lmr xxx:xxx` | 添加一个生图描述词，格式为`lm添加 触发词:描述词` |
| `lm帮助` or `lmh` | 查看所有预设好的描述词，如手办化、Q版化、孤独的我、第一人称、玉足...  |
| `lmh xxx` | 查看某个触发词对应的的描述词，如`lmh 手办化` |

### 示例图

![download](https://github.com/user-attachments/assets/3857e6a6-76f0-42f4-8ee0-00a91473c5f8)

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码

## 📌 注意事项

- 想第一时间得到反馈的可以来作者的插件反馈群（QQ群）：460973561（不点star不给进）
- 另外，推荐加入手办化bot集中营，里面有着各路来的手办化bot，方便交流经验、共享资源。
- nano-banana模型必须用图床上传图片，其他模型可以不用

<img width="1895" height="751" alt="图片" src="https://github.com/user-attachments/assets/a14e8d08-01f5-40db-9726-808bfc5bd44d" />

## 🤝 鸣谢

- [LMArena.ai](https://lmarena.ai/) - 模型竞技场, 网站上提供的海量先进测试大语言模型
- [LMArenaBridge](https://github.com/Lianues/LMArenaBridge)  - AI模型竞技场API代理器， 充当一座桥梁，让你能通过任何兼容 OpenAI API 的应用程序来使用 LMArena，欢迎大家前去[LMArenaBridge](https://github.com/Lianues/LMArenaBridge)点个star！
