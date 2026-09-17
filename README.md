# WeChat Analysis Write Publisher

A reusable AI skill for WeChat public-account content analysis, research, writing, review, formatting, and draft-box submission.

## Capabilities

- Analyze topics, source material, and audience needs.
- Build a traceable Research Pack before drafting factual claims.
- Draft and format WeChat-compatible articles.
- Render Markdown with 12 selectable editorial, minimal, technology, and lifestyle themes.
- Generate a visual theme gallery from the real article.
- Render dialogue, steps, timeline, statistic, comparison, quote, intro, and ending components.
- Normalize Chinese punctuation and CJK/Latin spacing, and convert external links to footnotes.
- Review factual support, copyright, privacy, safety, and AI disclosure.
- Validate a structured article bundle.
- Submit an approved article to the WeChat draft box after explicit authorization.

The skill does not automatically publish public posts.

## Repository structure

- `SKILL.md`: skill entry point and workflow.
- `agents/openai.yaml`: discovery and UI metadata.
- `references/`: schemas, review policy, and WeChat API guidance.
- `scripts/validate_bundle.py`: deterministic bundle validation.
- `scripts/formatter.py`: deterministic Markdown-to-WeChat inline HTML renderer.
- `scripts/gallery.py`: visual theme comparison using the real article.
- `scripts/theme_lint.py`: deterministic theme-schema validation.
- `scripts/wechat_adapter.py`: draft-box adapter with dry-run support.

## Validation

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
python3 -m py_compile scripts/*.py
```

## Status

Current version: `v0.3` — adds a 12-theme system, advanced layout components, a visual gallery, and theme validation.
