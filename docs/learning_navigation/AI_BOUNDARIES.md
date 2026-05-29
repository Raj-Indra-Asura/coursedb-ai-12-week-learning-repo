# AI Boundaries: Who Authors What

This document is the authoritative list of which files an AI assistant (or any
automation) may author versus which files the **learner** owns. It complements
[AI_USAGE_RULES.md](../../AI_USAGE_RULES.md).

The guiding principle:

> AI does the mechanical, infrastructure, and scaffolding work. The learner
> writes every piece of conceptual understanding, reflection, and exam answer.

## 🔴 Learner-owned — AI must NOT author the content

AI may add/repair headings, navigation links, TODO checklists, "self-check
questions" (questions only), and reference links. AI may **NOT** write the
explanations, reflections, narrative, or answers in these files:

| File / pattern | What stays the learner's |
| -------------- | ------------------------ |
| `weeks/week_*/theory_notes*.md` | All conceptual explanations |
| `weeks/week_*/reflection.md` | All reflections |
| `weeks/week_*/exercises.md` | The **answers** (AI may write the questions) |
| `weeks/week_*/mistakes_to_expect.md` | Detailed write-ups (AI may seed titles only) |
| `LEARNING_LOG.md` | Weekly entries (AI may extend the template only) |
| `docs/portfolio/portfolio_case_study.md` | The narrative (structure/prompts only) |
| `docs/portfolio/demo_script.md` | The script (skeleton only) |

If any of these files are missing, AI creates them as **blank templates only**
(headings + prompts + checkboxes) with a top comment:
`DO NOT auto-fill. This file is for the learner.`

## 🟢 AI/automation-allowed — AI may complete these fully

| Area | Examples |
| ---- | -------- |
| Infrastructure | `docker-compose.yml`, `scripts/init_db.sql`, `Makefile`, `pyproject.toml` |
| Migrations | `alembic/`, `docs/architecture/migrations.md` |
| Backend code | `app/api/*`, `app/services/*`, `app/db/*` |
| Tests | `app/tests/**`, `dbms_internals/*/tests/**` |
| CI | `.github/workflows/ci.yml` |
| Auto-generated docs | API docs (OpenAPI), constraints report, ER skeleton, SQL catalog |
| Evaluation harness | `scripts/run_evaluation.py`, `data/evaluation/*` |
| Question banks | exam-prep & self-check **questions** (never answers) |
| Verification | `VERIFICATION_REPORT.md` |

## 🟡 Mixed — AI provides structure, learner provides prose

These `docs/` files are created by AI as **structured templates** (headings,
tables to fill, Mermaid diagram skeletons, `> **TODO(learner):**` markers). The
conceptual prose is written by the learner:

- `docs/architecture/system_architecture.md`
- `docs/normalization/*.md`
- `docs/indexing/*.md`
- `docs/transactions/*.md`
- `docs/semantic_search/*.md`
- `docs/evaluation/*.md` (rubric tables provided; scores are the learner's)

## How to tell which bucket a file is in

1. Does the file capture the learner's understanding, opinion, or exam answer?
   → **Learner-owned** (🔴).
2. Is it code, config, tests, or generated-from-source documentation?
   → **AI-allowed** (🟢).
3. Is it a `docs/` conceptual write-up that needs a consistent structure?
   → **Mixed** (🟡): AI builds the skeleton, learner fills the prose.

When in doubt, default to treating the file as learner-owned and leave a
`> **TODO(learner):**` marker instead of writing content.
