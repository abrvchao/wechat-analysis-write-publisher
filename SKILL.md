---
name: wechat-analysis-write-publisher
description: Analyze topics and sources, draft, fact-check, review, format, and optionally submit articles to a WeChat public account draft box. Use for 公众号选题分析、资料研究、文章创作、排版、草稿包生成或经确认后写入草稿箱；不用于自动公开发布。
---

# WeChat Analysis Write Publisher

Produce a reviewable article package from a topic or source set. Default to **Draft mode**: stop at a validated local draft bundle unless the user explicitly authorizes a draft-box API write in the current task.

## Modes

- `manual`: research, write, review, and return the article package.
- `draft` (default): also format WeChat-compatible HTML and validate the bundle.
- `submit-draft`: upload assets and create a WeChat draft only after explicit confirmation, credentials are configured, and validation passes.

Never publish publicly. A request to publish is outside this skill; stop after creating the draft and ask the user to review it in WeChat.

## Workflow

1. Establish topic, audience, objective, voice, constraints, and provided sources. Infer ordinary editorial choices; ask only when a missing choice materially changes the result. If the input is a Radar seed research pack, preserve its explicit audience/objective and do not silently replace them.
2. Build or complete a Research Pack before drafting factual claims. Separate sourced facts, interpretations, and unresolved claims. If a compatible Radar seed pack is provided, treat it as grounded starting evidence rather than a finished article brief: preserve source IDs/provenance, keep [Radar interpretation] items as interpretation, and research unresolved evidence gaps before turning them into factual claims. For current or consequential facts, use primary sources where possible.
3. Choose an angle and outline. Avoid duplicating source structure or close paraphrase.
4. Draft title candidates, digest, body, CTA, and source notes. Facts in the article must trace to the Research Pack; clearly label opinion or inference.
5. Review for factual support, copyright risk, sensitive claims, privacy, promotional overstatement, unsupported medical/legal/financial advice, and AI-generated-content disclosure needs.
6. Read [references/formatting.md](references/formatting.md). If the user has not chosen a style, recommend three themes or generate `scripts/gallery.py` using the real article. Apply layout components sparingly, then render WeChat-safe inline HTML with `scripts/formatter.py`.
7. Create `research_pack.json`, `article.json`, `content.html`, and `review.json` according to [references/schemas.md](references/schemas.md), then run `scripts/validate_bundle.py`.
8. If `submit-draft` is authorized, read [references/wechat-api.md](references/wechat-api.md), use `scripts/wechat_adapter.py`, and return the API result plus a redacted operation log. Never print secrets or access tokens.

## Radar seed handoff

This skill may receive a research_pack.json produced by the Content Opportunity Radar adapter. Compatible packs include a forward-compatible radar_handoff object with handoff_type: "radar_seed_research_pack".

When present:

- preserve the Radar source IDs and radar_* provenance fields; do not rewrite a source into a stronger source class or credibility level;
- treat Radar metric claims as observations scoped to their cited source, not universal facts;
- keep [Radar interpretation] entries in insights as interpretation unless independent sources support a factual restatement;
- treat [Evidence gap] entries and other open_questions as unresolved research work, not facts to fill by inference;
- if new sources are added during writing research, append new source/claim IDs rather than changing the meaning of existing IDs;
- article factual claims still require source IDs after any additional research; the normal review and citation gates remain unchanged;
- the Radar handoff never authorizes draft-box submission or public publishing.

## Required gates

- Block submission if the review status is `blocked`, required citations are missing, the cover asset has no `media_id`, or `WECHAT_APP_ID` / `WECHAT_APP_SECRET` are absent.
- Treat external API submission as a mutation. Confirm the target account and obtain current-task authorization immediately before the call.
- Never silently retry a draft creation request after an ambiguous network failure; first determine whether a draft was created.
- Do not claim that content reached the draft box unless the API returned a successful media identifier.
- Do not upload sources, private notes, or credentials as article content.
- Run `scripts/theme_lint.py` after theme changes. Do not include scripts, forms, external trackers, remote CSS, or unsupported interactive elements in article HTML.

## Supervisor handoff

Return a compact status object containing: `mode`, `topic`, `angle`, `artifacts`, `review_status`, `risk_flags`, `submission_status`, `draft_media_id`, and `next_action`. Escalate unresolved factual disputes or high-impact compliance issues to a human reviewer.

For schemas and acceptance criteria, read [references/schemas.md](references/schemas.md). For disclosure and review rules, read [references/review-policy.md](references/review-policy.md). For Markdown rendering and theme selection, read [references/formatting.md](references/formatting.md).
