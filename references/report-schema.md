# 呈现数据接口

`scripts/render_report.py` 只负责展示，不采集聊天，不替 agent 计算统计或生成判断。先完成采集、分析和核对，再写数据。字段全部是纯文本；模板用 textContent 渲染，不接受 HTML 注入。

```json
{
  "year": 2025,
  "title": "把念头，做成看得见的东西。",
  "subtitle": "你的个人年度回顾",
  "period": "2025.01.01 — 2025.12.31 · 虚构结构示例",
  "coverage": "依据已读取的项目与聊天；部分历史正文未开放。",
  "demo": false,
  "chapters": [
    {
      "id": "chapter-01",
      "eyebrow": "01 / 足迹",
      "title": "这一年，留下了一些作品。",
      "body": "写有证据的具体内容，避免空泛感言。",
      "tone": "dark",
      "metrics": [{"value": "7", "label": "可识别项目", "note": "按稳定项目 ID 去重"}],
      "projects": [{"name": "项目名", "description": "具体问题与产物", "status": "已交付，发布未验证"}],
      "quote": {"text": "经过原文核对的短引用", "attribution": "用户 · 2025.04.18"},
      "sources": [{"id": "e-001", "label": "2025.04.18 · 项目讨论", "locator": "session-id / message-id"}]
    }
  ],
  "closing": "有些故事，还在继续。"
}
```

必填根字段：`year`（整数）、`title`、`period`、`coverage`、`chapters`（至少一章）；必填章节字段：唯一 `id`、`title`、`body`。其余可省略。`tone` 可为 `dark`、`light`、`sage`、`blue`、`coral`、`pink` 或 `yellow`。章节可只带正文，不必硬填数字、项目或引用；每章最多两项补充指标，更多细节进入依据弹窗。

## 动态报告扩展

`hero` 是大数字或模型名称；使用实际数值而非预先四舍五入的字符串，模板负责显示与数字递增。`metrics` 仍为最多两个补充值。章节可添加 `note`（短范围说明）、`tags`（短标签）、`bars`（真实贡献比较）或 `distribution`（主类分布）。

```json
{"id":"token-total","kind":"total","tone":"blue","title":"这一年，留下了可核验的投入。","body":"来自已读取日志的输入与输出。","hero":{"value":12345678,"scale":10000,"decimals":1,"suffix":"万","label":"可核验 token"},"note":"含缓存输入；尚未开放的来源不计入。"}
```

模型名用 `hero:{"text":"真实 model ID","label":"按有效响应记录数排名"}`。`bars` / `distribution` 是 `{label,value,color}` 数组，值非负且合计大于零，color 为六位十六进制；bars 可加 `display`。

根字段 `summary` 用于最后一屏：`{portrait,body,tags,metrics,note,sources,tone}`。metrics 推荐 4–6 项，使用简短字符串；较长值可设 `small:true`。画像从真实行为归纳。`project_index` 用于全局作品索引按钮，字段为 `{name,description,status,evidence_ids}`。`downloads` 是 `{label,href}` 数组，只用安全本地相对路径。

不要用 `cover`、`closing`、`next`、`prev` 等 UI 保留名作为章节 id。旧结构的正文、项目和引用仍可显示；新报告优先用大数字、短句与最后一屏统计画像。

`sources` 指向 evidence.jsonl 中的 ID，label 面向读者，locator 显示可核验位置。原话和醒目数字应有对应 sources。模板有示例水印，`demo=true` 永远明确显示「虚构示例 · 非个人数据」。实际报告使用 `demo=false`，不得保留示例统计或引用。

模板不是统计图工具。如添加时间序列，使用核验过的月度数据，未知月份留空，说明口径，不要为装饰画虚假曲线。最终 `report.md` 与 HTML 使用相同叙事、统计与范围说明。


## 用量与分享卡扩展

`monthly_usage`：每月一项 `{month,tokens,messages,future,token_display}`，month=1…12，未知用量为null，不是0。`usage_source`为来源短标签；`usage_note`、`message_source_label`与`message_note`分别标注Token与消息口径。`project_usage`支持待补充项目列表 `{name,tokens,display}`；真实排名用按实际Token降序的`bars`。

`summary`可加`display_title`（如「我的 GPT\n年度报告」）；`share_card`支持`hero:{value,unit,label}`、`project_types`、`project_examples`、`persona_description`、`metrics`（最多4项精选统计）、`display_date`。字段来自当前用户证据，不带任何真实用户的默认数据。`artwork.src`可省略，卡片会隐藏人物区域；有权限与工具时为该用户另生成角色。

`music:{src,title,artist,license,autoplay}`，路径为本地素材，播放遵守浏览器手势政策。`share_card.download_data`可放已核验PNG的内嵌URI，使离线一键下载可用。
