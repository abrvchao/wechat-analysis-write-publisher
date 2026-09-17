# WeChat Analysis Write Publisher

A reusable AI skill for WeChat public-account content analysis, research, writing, review, formatting, and draft-box submission.

## Capabilities

- Analyze topics, source material, and audience needs.
- Build a traceable Research Pack before drafting factual claims.
- Draft and format WeChat-compatible articles.
- Review factual support, copyright, privacy, safety, and AI disclosure.
- Validate a structured article bundle.
- Submit an approved article to the WeChat draft box after explicit authorization.

The skill does not automatically publish public posts.

## Repository structure

- `SKILL.md`: skill entry point and workflow.
- `agents/openai.yaml`: discovery and UI metadata.
- `references/`: schemas, review policy, and WeChat API guidance.
- `scripts/validate_bundle.py`: deterministic bundle validation.
- `scripts/wechat_adapter.py`: draft-box adapter with dry-run support.

## Validation

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
python3 -m py_compile scripts/*.py
```

## Status

Current version: `v0.1` — usable foundation, intended for continued iteration.
