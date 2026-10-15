# Yearsona 统一3D潮玩风格

这是所有用户共用的画风规范，不是统一复制一个人的外貌。每次制作都主动调用可用图像工具，并把 `assets/yearsona-style-reference.png` 作为风格参考，不等待用户额外提出。不得将已有个人报告的公仔复制到其他用户输出。

## 固定不变

- 原创3D人形搪胶/树脂收藏公仔，精致实体玩具产品渲染，不是机器人、扁平SVG、线稿、低多边形、毛绒或写真人像。
- 大头小身；头部约占角色高度45%—55%，圆润脸颊、微小鼻口、明亮深色大眼睛、雕塑感头发、柔和表情。
- 奶油白、海军蓝为基调，少量暖珊瑚/金色点缀；配色可在此基础上微调，不更换整体色彩语言。
- 柔和哑光搪胶/树脂，眼睛细腻高光，衣褶、鞋底和小配件有真实体积；暖色柔光、细腻环境遮蔽，边缘干净。
- 单角色完整全身，正面略三分之四视角，小型奶油色收藏底座，主体周围留5%—8%空间。原生透明PNG；不把棋盘格烘焙进背景，不带文字、标识、水印或整张海报。

## 根据记录变化

从有证据的年度主题选择1—2个配件及姿态：创作可用素色画笔、学习可用空白书本、开发可用简洁工具、音乐可用无品牌乐器。服装细节、配件、站姿/坐姿可定制，但材质、比例、表情语言和灯光必须保持固定规范。不得从聊天猜测用户真实性别、年龄、肤色、长相；用户未指定外观时使用虚构角色设计，并说明非本人肖像。

## 可直接使用的提示词骨架

```text
Create one original premium collectible 3D chibi HUMAN vinyl/resin figurine.
Use the attached Yearsona reference for STYLE ONLY: head-to-body proportion,
sculpted rounded hair, softly blushed cheeks, large glossy dark eyes, tiny nose,
subtle friendly smile, cream/navy outfit, tiny coral/gold accents, satin-matte
vinyl material, soft warm studio lighting, nuanced ambient occlusion, detailed
rounded clothing folds and chunky sneakers. Full body on a small ivory pedestal,
front three-quarter view, centered portrait composition, transparent alpha PNG,
5–8% clear margin, no text, no logos, no watermark.
Invent a fictional character; this is not the user's actual likeness.
Personalize ONLY these content details from the annual summary:
[verified creative themes, 1–2 symbolic accessories, pose, restrained outfit detail].
Do not copy a previous user's face, hair, accessories, projects or exact figurine.
Do not switch to robot, SVG, 2D illustration, anime lineart, plush or photorealism.
```

调用后检查不是平面画风、背景alpha有效、全身完整、没有额外人物、配件有依据。失败时针对问题修正提示词重试一次；仍受工具或权限限制时保留原因，不循环调用或偷偷切到需要用户密钥的API。

## 无生图能力时

包内参考图是新生成的通用虚构风格样例，不来自任何用户的个人公仔。渲染器可自动复制它来保持预览的3D画风，但必须保存 `method=bundled-reference`、`generation_status=needs-personalization`，末页注明“通用3D风格参考 · 专属形象待生成”。这不是专属生成完成，不得把参考图当作每个人的新形象。

有图像工具时必须优先完成专属生成，保存提示词和工具说明到本次报告，而非技能包。最终 `artwork` 指向真实生成的文件，`method=image-tool`，并设置 `generation_status=complete`。然后渲染卡片、导出PNG、重新渲染报告；末页揭晓动画只负责呈现，不伪装模型调用。
