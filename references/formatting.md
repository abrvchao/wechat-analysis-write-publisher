# WeChat formatting

Use `scripts/formatter.py` when the task includes 排版, 微信格式, HTML preview, or draft submission.

## Themes

- `editorial`: serious analysis, interviews, reports, and long-form essays.
- `minimal`: reflective writing, personal essays, and low-noise reading.
- `tech`: tutorials, product reviews, AI, software, and tool roundups.

Choose from the article's subject unless the user specifies a theme. Preserve the author's wording: formatting may normalize punctuation and spacing but must not rewrite claims.

## Supported Markdown

Headings, paragraphs, bold text, inline code, fenced code, ordered and unordered lists, blockquotes, images, links, horizontal rules, and callouts written as `> [!tip]`, `> [!important]`, or `> [!warning]`.

External links become numbered footnotes because WeChat may not preserve ordinary external anchors. Images remain `<img>` elements for later upload and URL replacement.

## Command

```bash
python3 scripts/formatter.py article.md --theme editorial --output content.html
```

Run `validate_bundle.py` after building the complete article bundle. Visual approval is still required before draft submission.

## Design provenance

The separation of content analysis, theme choice, inline rendering, compatibility normalization, and draft submission was informed by the public project `xiaohuailabs/xiaohu-wechat-format`. This repository uses an independent standard-library implementation and does not copy its code or theme assets. Its README describes an MIT license, but no root `LICENSE` file was retrievable during the V0.2 review, so only general workflow ideas were adopted.
