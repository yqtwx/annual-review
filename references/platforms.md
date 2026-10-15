# macOS、Windows 与 Linux

技能内容不依赖操作系统。macOS 使用 `python3`；Windows 使用可用的 `python` 或 `py -3`。Python 3.9+，渲染和基础形象只用标准库。不要假设存在 Edge、PowerShell、盘符或本机固定运行时。

## 安装与数据

macOS/Linux 默认技能根为 `${CODEX_HOME:-$HOME/.codex}/skills`；Windows 默认 `%USERPROFILE%\.codex\skills`。先用宿主确认实际 CODEX_HOME。技能目录名必须是 `yearsona`。macOS 安装示例：

```sh
git clone https://github.com/yqtwx/yearsona.git "${CODEX_HOME:-$HOME/.codex}/skills/yearsona"
```

仓库、技能目录与调用名统一为 `yearsona`。输出选择用户可写目录，不能输出到技能安装目录。路径始终引用，允许中文、空格；HTML资源使用正斜杠相对路径，打开本地文件用 `Path.resolve().as_uri()`，不拼接 `file://`。

有明确授权的本地 Codex 数据可检查实际 CODEX_HOME 下的 `sessions`、`archived_sessions`，先验证存在及内容格式，再各自分析并按稳定会话ID去重；不要假设每个平台都有相同目录。ChatGPT历史仅从当前工具、导出或用户明确指定来源获取。不要把 macOS 应用容器、Keychain 或浏览器资料当作聊天数据扫描。

## 统一形象流水线

1. 先生成有依据的 summary、tags、project_types，调用可用图像生成工具生成原创潮玩透明图，保存到本次报告 `assets/`，填写 `artwork.src/alt/method`。
2. 没有工具或生成失败时继续渲染。`render_report.py` 自动调用 `persona.py` 复制包内通用3D参考图以维持统一画风，标明 `method=bundled-reference`、`generation_status=needs-personalization`；不能声称是图像模型产物。标准完成条件是实际生成用户专属3D潮玩；参考图只用于无图像工具时的未完成预览，不能宣布完整交付。
3. 主报告与独立卡片都必须有角色。主报告只有末页出现；第一次进入先揭晓进度，再呈现。渲染同时输出 `.prepared.json` 与 `annual-card.html`；不要继续使用缺少自动补全素材的旧JSON。
4. 用宿主浏览器能力导出卡片PNG；若没有可调用浏览器，使用下方跨平台脚本。最后把导出数据重新渲染到主报告。不能把插画SVG改名为PNG或把生成进度动画当作图像生成调用。

## PNG 导出

优先使用已有浏览器工具；没有时可在用户允许安装依赖的环境中安装可选依赖：

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/render_report.py --data reports/report-data.json --output reports/report.html
python3 scripts/export_card.py --html reports/annual-card.html --png reports/annual-card.png --data reports/report.prepared.json
python3 scripts/render_report.py --data reports/report.prepared.exported.json --output reports/final-report.html
```

Windows 将 `python3` 换为 `python`。Apple Silicon 与 Intel 都使用 Playwright 自己匹配的浏览器，不指定 x86 或Windows可执行文件。也可用 `--browser-executable "<existing-chromium-path>"`；Safari不是Chromium，不能把Safari应用路径传入。

PNG导出不是基础渲染的依赖；不可安装浏览器时仍需交付带卡通形象的HTML及独立卡片，明确PNG导出缺口，不能宣称完整交付。已有文件仅用明确的 `--force` 覆盖。

浏览器音乐自动播放与 `file://` 下载受平台策略限制；首次点击/键盘可启动音乐，关闭后不可自动恢复。导出数据包含PNG数据URI，用来支持本地下载。macOS检查Chrome/Safari阅读、中文字体、触控板滚动、上下方向键、保存文件、系统减少动态效果；没有Mac设备时应明确实机验证缺口，不能把桌面缩放模拟说成Mac实测。
