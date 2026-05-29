# Verification Report

_Generated as part of the AI infrastructure work (blocks B1–B11). This report
states the **true** state of the repository, without inflated completion claims.
Where something is incomplete or deferred to the learner, it is listed with the
exact file path._

Date: 2026-05-29

## How this was verified

- Ran `pytest` with coverage in the project virtualenv.
- Ran `ruff check .` and `black --check .` repo-wide.
- Started `pgvector/pgvector:pg16` via Docker and ran `alembic upgrade head`,
  `scripts/setup_db.py`, `scripts/seed_data.py`, and
  `scripts/smoke_test_semantic_search.py` against it.
- Checked file existence and whether learner-owned files remain templates.

> **Sandbox caveat:** `sentence-transformers`/`torch` could not be installed in
> the build environment (the PyTorch download host is blocked). The embedding
> service therefore falls back to a **deterministic hashing encoder**. All
> pipeline wiring is exercised end-to-end; real model quality must be confirmed
> by the learner once the model is available locally / in CI.

## Part D checklist

| Check | Status | Notes |
| ----- | ------ | ----- |
| `docker-compose up -d` starts Postgres + pgvector | ✅ | `pgvector/pgvector:pg16`; `scripts/init_db.sql` creates `vector` + `pg_trgm`. |
| `alembic upgrade head` builds schema from zero | ✅ | Migration `f0f92986b448` creates all 10 tables + extensions. |
| `python scripts/setup_db.py` is idempotent | ✅ | `CREATE ... IF NOT EXISTS`; IVFFlat gated on row count. |
| `python scripts/seed_data.py` loads sample data | ✅ | 3 courses, 19 topics, 10 questions, 7 resources, 4 users. |
| `python scripts/generate_embeddings.py` produces rows | ✅ | Idempotent; inserts into `chunk_embeddings`. Uses hashing encoder in this env. |
| `python scripts/smoke_test_semantic_search.py` prints PASS | ✅ | Asserts top-1 for 3 distinct chunks; prints `PASS`. |
| `pytest -q` runs and all tests pass | ✅ | **126 passed, 1 skipped** (skipped = embedding test needing cached model). |
| Coverage ≥ 70% on `app/` and `dbms_internals/` | ✅ | **77%** total. |
| `ruff check . && black --check .` clean | ✅ | All checks pass; 51 files unchanged by black. |
| CI workflow runs green on push | ⚠️ | `.github/workflows/ci.yml` added (lint/test/migrate jobs). Not yet observed running on GitHub; verify the first run. |
| README "Current Progress" reflects reality | ✅ | Rewritten to list infra-complete vs learner-pending. |
| PART A files remain empty templates | ✅ | No AI-authored prose added; see below. |
| `VERIFICATION_REPORT.md` lists remaining learner TODOs | ✅ | This document. |

## Test summary

```
126 passed, 1 skipped
coverage: 77% (app/ + dbms_internals/)
```

Test files present (18):
- `app/tests/api/`: health, courses, topics, questions, resources, search,
  analytics, learning
- `app/tests/services/`: chunking, embedding, semantic_search, sql_search
- `app/tests/db/`: models
- `dbms_internals/*/tests/`: bplus_tree, hash_index, wait_for_graph

Lowest-covered modules (candidates for more tests, none below requirement
overall):
- `app/services/semantic_search_service.py` — 100% (unit-tested via mocked DB session)
- `app/api/questions.py` — 50%
- `app/api/resources.py` — 53%

## Block-by-block status

| Block | Description | Status |
| ----- | ----------- | ------ |
| B1 | Docker + DB bootstrap, Makefile, pyproject | ✅ Complete |
| B2 | Alembic migrations + `docs/architecture/migrations.md` | ✅ Complete |
| B3 | Implement stubbed backend methods/endpoints | ✅ Complete |
| B4 | Semantic-search pipeline end-to-end + smoke test | ✅ Complete |
| B5 | Test suite + coverage + CI | ✅ Complete (CI un-observed) |
| B6 | `docs/` scaffolds + auto-generated reference docs | ✅ Complete |
| B7 | Evaluation harness | ✅ Complete |
| B8 | Missing syllabus theory **skeletons** | ✅ Complete (questions only) |
| B9 | Exam-prep question bank | ✅ Complete (questions only) |
| B10 | CONTRIBUTING + AI_BOUNDARIES + README | ✅ Complete |
| B11 | This verification report | ✅ Complete |

## Learner-owned files left as templates (PART A — intentionally NOT authored)

These remain empty / template-only by design. They are the learner's to write:

- `weeks/week_*/theory_notes.md` (all 12) and the new supplements:
  - `weeks/week_09_transactions/theory_notes_recovery.md` — skeleton only
  - `weeks/week_12_evaluation_portfolio/theory_notes_distributed.md` — skeleton only
  - `weeks/week_12_evaluation_portfolio/theory_notes_semi_structured.md` — skeleton only
  - `weeks/week_12_evaluation_portfolio/theory_notes_oo_object_relational.md` — skeleton only
  - `weeks/week_12_evaluation_portfolio/theory_notes_nosql_intro.md` — skeleton only
  - `weeks/week_06_advanced_sql/theory_notes_access_control.md` — skeleton only
- `weeks/week_*/reflection.md` (all 12) — reflections pending
- `weeks/week_*/exercises.md` — answers pending (questions present)
- `weeks/week_03_er_modeling/exercises_relational_algebra.md` — 5 problems, answer blanks
- `LEARNING_LOG.md` — weekly entries pending
- `docs/portfolio/portfolio_case_study.md` — narrative pending
- `docs/portfolio/demo_script.md` — script pending
- `weeks/week_*/mistakes_to_expect.md` — detailed write-ups pending

## `docs/` templates awaiting learner prose (PART B6 — structure done, content pending)

Each of these has a complete structure (headings, tables, Mermaid skeletons) and
`> **TODO(learner):**` markers. The conceptual prose is pending:

- `docs/architecture/system_architecture.md`
- `docs/normalization/normalization_report.md`, `fd_analysis.md`, `anomaly_examples.md`
- `docs/sql/views_and_triggers.md`
- `docs/indexing/indexing_notes.md`, `bplus_tree_explanation.md`, `hash_index_explanation.md`, `query_plan_analysis.md`
- `docs/transactions/transaction_notes.md`, `acid_examples.md`, `concurrency_problems.md`
- `docs/semantic_search/semantic_search_report.md`, `embeddings_explained.md`
- `docs/evaluation/evaluation_report.md`, `semantic_search_evaluation.md`, `performance_benchmarks.md`

Fully completed (auto-generated or maintainer-owned) docs:
- `docs/architecture/migrations.md`, `docs/architecture/api_documentation.md`
- `docs/sql/constraints_report.md`, `docs/sql/sql_query_catalog.md`
- `docs/er_diagrams/coursedb_ai_er_design.md`
- `docs/evaluation/rubric.md`

## Remaining gaps / follow-ups

1. **Real embedding model not validated here.** Install
   `sentence-transformers` locally/CI and re-run
   `scripts/generate_embeddings.py` + `scripts/smoke_test_semantic_search.py`
   to confirm relevance with the real model (current results use the hashing
   fallback).
2. **CI not yet observed green.** `.github/workflows/ci.yml` is committed but
   its first GitHub-hosted run should be checked; the `test` job installs a
   lightweight dependency subset (no torch) and relies on the embedding test
   being skipped when the model is uncached.
3. **Vector-path coverage** for `semantic_search_service.py` is now 100% via
   mocked-DB unit tests covering `search`, `search_by_course`,
   `compare_with_keyword_search`, `get_similar_chunks`, and `hybrid_search`
   (result formatting, merging, and score normalization). The live `<=>`
   similarity ordering still needs a real pgvector instance to validate;
   consider adding `requires_pgvector`-marked integration tests in CI's
   `migrate` job.
4. **All learner-owned content above is pending** — by design, not a defect.
