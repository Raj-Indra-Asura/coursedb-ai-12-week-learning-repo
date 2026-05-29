# Contributing to CourseDB-AI

Thank you for your interest in this repository. This is a **learning-first**
portfolio project, so the contribution rules are a little different from a
typical open-source project.

## The learning-first contract

This repository documents a learner's journey through a DBMS + AI course. The
single most important rule:

> **AI assistants and contributors must NOT author the learner's conceptual
> content, reflections, exam answers, or personal narrative.**

See [AI_USAGE_RULES.md](AI_USAGE_RULES.md) and
[docs/learning_navigation/AI_BOUNDARIES.md](docs/learning_navigation/AI_BOUNDARIES.md)
for the exact list of files that are owned by the learner versus the files that
AI/automation may complete.

In short:
- **Learner-owned** (templates only, never pre-filled): `weeks/week_*/theory_notes*.md`,
  `weeks/week_*/reflection.md`, `weeks/week_*/exercises.md` answers,
  `LEARNING_LOG.md` weekly entries, the portfolio narrative, and hand-drawn
  diagrams.
- **AI/automation-allowed**: infrastructure, glue code, tests, migrations,
  auto-generated docs, scaffolds, and question banks (questions only).

## How to set up locally

```bash
make up        # start Postgres + pgvector
make migrate   # alembic upgrade head
make seed      # load sample data
make test      # run pytest with coverage
make lint      # ruff + black --check
```

## How to add a new week

1. Create `weeks/week_NN_<topic>/` with the standard files:
   `theory_notes.md`, `exercises.md`, `reflection.md`, `mistakes_to_expect.md`,
   `README.md` (use existing weeks as the structure reference).
2. Leave learner-owned files as **templates only** (headings, prompts,
   checkboxes, self-check questions — no answers or explanations).
3. Add any SQL under the week folder so it is picked up by the SQL catalog
   generator.
4. Link the new week from `README.md` and `LEARNING_LOG.md` navigation.

## How to add tests

- Tests live under `app/tests/` (mirroring `app/`) and
  `dbms_internals/*/tests/`.
- Follow the **AAA** pattern (Arrange, Act, Assert), keep tests deterministic,
  and make **no network calls**.
- Use the fixtures in `app/tests/conftest.py` (`test_db`, `client`,
  `sample_course`, etc.). Mark tests that need a real vector DB with
  `@pytest.mark.requires_pgvector`.
- Every new code file must come with at least one test and must not break
  existing tests. Target ≥ 70% coverage on `app/` and `dbms_internals/`.

## Commit convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
```

Common types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `ci`.
For the AI infrastructure blocks, prefix with the block id, e.g.
`[B5] test: add analytics API tests`.

## Code quality bar

- Python: type hints, docstrings (Google/NumPy style), `logging` (no `print()`)
  in library code.
- SQL: **UPPERCASE** keywords (match the existing files).
- Run `make lint` and `make test` before committing.
- No new runtime dependencies unless necessary; pin the version and justify it
  in the commit message.
- Leave human TODOs as `# TODO(learner):` in code or
  `> **TODO(learner):**` in markdown.
