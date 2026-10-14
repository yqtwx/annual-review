# Annual Review · 我的 GPT 年度报告

把可访问的年度项目与聊天整理成有故事感的个人 AI 年报。短文案、大数字、原创装饰、逐屏动效，以及可以保存分享的 9:16 镭射卡片。

## 功能

- 总 Token、用量峰值、项目排行、月度消耗与常用模型：只计算实际可用的数据。
- 代表作品、创作类型、反复打磨的项目，以及 GPT 在日常中的角色。
- 上下翻页、数字递增、末页角色揭晓；遵循系统减少动效偏好。
- 可选原创潮玩形象与免费许可音乐；音乐以右上角圆形图标控制。
- 独立分享卡 HTML/PNG、离线报告、证据索引与覆盖范围说明。

这是个人回顾技能，不是公司财务报告，也不是 OpenAI 官方年度报告。

## 安装到 Codex

下载仓库源码，将完整文件夹命名为 `annual-review`，放入技能目录。保留 `SKILL.md`、`agents`、`assets`、`references` 和 `scripts`。

| 系统 | 默认技能目录 |
| --- | --- |
| Windows | `%USERPROFILE%\.codex\skills\annual-review` |
| macOS / Linux | `~/.codex/skills/annual-review` |

使用自定义 `CODEX_HOME` 时，放入该目录的 `skills/annual-review`。其他支持 `SKILL.md` 的 agent 使用各自技能目录；数据入口和权限由宿主提供。

## 使用

```text
用 $annual-review 回顾我今年可访问的项目与聊天，生成我的 GPT 年度报告。
```

可以指定年份、时区、数据来源和视觉风格，例如「只统计 ChatGPT，做一份有音乐年度回顾节奏的报告，最后生成潮玩形象与分享卡」。

## 数据与隐私

安装技能不会扩大账号或历史记录的访问权限。它使用宿主已提供的接口、用户授权的本地记录或官方导出。数据不完整时说明覆盖范围，不根据聊天长度猜测 Token，也不按比例分摊缺失明细。

累计用量与年度用量、不同平台数据分别记录；项目的日期跨度不是工作时长。个人报告、日志、头像、生成形象和音乐保存到独立输出目录，不进入技能仓库，也不会自动上传或发布。

仓库不携带任何真实用户的姓名、聊天、项目、统计或个人素材。设计预览中的作品、数字和台词均为明确标注的虚构示例。

## 本地设计预览

渲染脚本只依赖 Python 标准库。使用 Python 3.9 或更高版本，在仓库目录执行：

```sh
python scripts/render_report.py --demo --output reports/preview.html
python scripts/render_report.py --demo --card --output reports/card.html
```

打开生成的 HTML 即可查看。图片生成、音乐搜索、截图和 PNG 导出依赖当前 agent 的可用工具；浏览器阻止音乐自动播放时，首次用户交互会启动，用户关闭后不会因翻页重新播放。

## 仓库结构

```text
SKILL.md       技能入口
agents/        技能显示信息
references/    采集、统计、设计与数据结构
scripts/       用量分析与离线渲染
assets/        HTML、CSS、交互与分享卡模板
```
