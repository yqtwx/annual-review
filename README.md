# Yearsona · 年度造像

把可访问的年度项目与聊天整理成有故事感的个人 AI 年报。短文案、大数字、原创装饰、逐屏动效，以及可以保存分享的 9:16 镭射卡片。

## 功能

- 总 Token、用量峰值、项目排行、月度消耗与常用模型：只计算实际可用的数据。
- 代表作品、创作类型、反复打磨的项目，以及 GPT 在日常中的角色。
- 上下翻页、数字递增、末页角色揭晓；遵循系统减少动效偏好。
- 每份报告自动提供专属原创卡通/潮玩形象；可选免费许可音乐；音乐以右上角圆形图标控制。
- 独立分享卡 HTML/PNG、离线报告、证据索引与覆盖范围说明。

这是个人回顾技能，不是公司财务报告，也不是 OpenAI 官方年度报告。

## 安装到 Codex

下载仓库源码，将完整文件夹命名为 `yearsona`，放入技能目录。保留 `SKILL.md`、`agents`、`assets`、`references` 和 `scripts`。

| 系统 | 默认技能目录 |
| --- | --- |
| Windows | `%USERPROFILE%\.codex\skills\yearsona` |
| macOS / Linux | `~/.codex/skills/yearsona` |

使用自定义 `CODEX_HOME` 时，放入该目录的 `skills/yearsona`。其他支持 `SKILL.md` 的 agent 使用各自技能目录；数据入口和权限由宿主提供。

## 使用

```text
用 $yearsona 回顾我今年可访问的项目与聊天，生成我的 GPT 年度报告。
```

可以指定年份、时区、数据来源和视觉风格，例如「只统计 ChatGPT，做一份有音乐年度回顾节奏的报告，最后生成潮玩形象与分享卡」。

## 数据与隐私

安装技能不会扩大账号或历史记录的访问权限。它使用宿主已提供的接口、用户授权的本地记录或官方导出。数据不完整时说明覆盖范围，不根据聊天长度猜测 Token，也不按比例分摊缺失明细。

累计用量与年度用量、不同平台数据分别记录；项目的日期跨度不是工作时长。个人报告、日志、头像、生成形象和音乐保存到独立输出目录，不进入技能仓库，也不会自动上传或发布。

仓库不携带任何真实用户的姓名、聊天、项目、统计或个人素材。设计预览中的作品、数字和台词均为明确标注的虚构示例。

## 本地设计预览

渲染脚本只依赖 Python 标准库。使用 Python 3.9 或更高版本，在仓库目录执行：

```sh
python3 scripts/render_report.py --demo --output reports/preview.html
python3 scripts/render_report.py --demo --card --output reports/card.html
```

打开生成的 HTML 即可查看。优先使用当前 agent 的图像生成工具；工具不可用时使用随包附带的通用3D风格参考图，并明确标注专属形象待生成，不冒充定制成品。PNG导出可使用跨平台Playwright脚本，音乐搜索依赖当前工具；浏览器阻止音乐自动播放时，首次用户交互会启动，用户关闭后不会因翻页重新播放。

## 仓库结构

```text
SKILL.md       技能入口
agents/        技能显示信息
references/    采集、统计、设计与数据结构
scripts/       用量分析与离线渲染
assets/        HTML、CSS、交互与分享卡模板
```

## macOS 与跨平台导出

macOS（Apple Silicon/Intel）使用 `python3`，Windows使用 `python` 或 `py -3`。基础渲染与3D基础图不需要第三方依赖。支持中文和空格目录，所有媒体以相对路径保存。

```sh
git clone https://github.com/yqtwx/yearsona.git "${CODEX_HOME:-$HOME/.codex}/skills/yearsona"
```

PNG导出（可选安装浏览器依赖）：

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/render_report.py --demo --output reports/preview.html
python3 scripts/export_card.py --html reports/annual-card.html --png reports/annual-card.png --data reports/preview.prepared.json
python3 scripts/render_report.py --data reports/preview.prepared.exported.json --output reports/final-preview.html
```

具体数据路径、浏览器策略与导出顺序见 [跨平台指南](references/platforms.md)。兼容性工作流在 macOS、Windows 和 Linux 运行交付回归测试；不等同于每个版本都已完成Safari实机测试。

项目已从通用名称 Annual Review 更名为 Yearsona，技能调用为 `$yearsona`。仓库、技能目录与调用名统一为 `yearsona`。
