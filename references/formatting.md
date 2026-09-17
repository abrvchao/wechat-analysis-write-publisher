# WeChat formatting

Use `scripts/formatter.py` when the task includes 排版, 微信格式, HTML preview, or draft submission.

## Themes

- Editorial: `editorial-red`, `newspaper`, `magazine`.
- Minimal: `ink`, `mint`, `wechat-green`.
- Technology: `tech-blue`, `github`, `midnight`.
- Lifestyle: `terracotta`, `lavender`, `amber`.

Choose from the article's subject unless the user specifies a theme. Preserve the author's wording: formatting may normalize punctuation and spacing but must not rewrite claims.

## Supported Markdown

Headings, paragraphs, bold text, inline code, fenced code, ordered and unordered lists, blockquotes, images, links, horizontal rules, and callouts written as `> [!tip]`, `> [!important]`, or `> [!warning]`.

External links become numbered footnotes because WeChat may not preserve ordinary external anchors. Images remain `<img>` elements for later upload and URL replacement.

## Command

```bash
python3 scripts/formatter.py article.md --theme editorial --output content.html
```

List themes or generate a visual gallery using the real article:

```bash
python3 scripts/formatter.py article.md --list-themes
python3 scripts/gallery.py article.md --output theme-gallery.html
```

## Layout components

Use fenced containers only when they materially improve the article:

- `:::intro[导读]` — opening summary.
- `:::dialogue[访谈]` — alternating dialogue bubbles.
- `:::steps[步骤]` and `:::timeline[时间线]` — numbered sequences.
- `:::stat[关键数据]` — metric cards.
- `:::compare[对比]` — comparison columns.
- `:::quote[金句]` — centered quote card.
- `:::end[CTA]` — ending marker and call to action.

Close each block with `:::`. Prefer one to three enhanced components per article; layout must serve comprehension rather than decoration.

Run `validate_bundle.py` after building the complete article bundle. Visual approval is still required before draft submission.

## Design provenance

The separation of content analysis, theme choice, inline rendering, compatibility normalization, and draft submission was informed by the public project `xiaohuailabs/xiaohu-wechat-format`. This repository uses an independent standard-library implementation and does not copy its code or theme assets. Its README describes an MIT license, but no root `LICENSE` file was retrievable during the V0.2 review, so only general workflow ideas were adopted.
