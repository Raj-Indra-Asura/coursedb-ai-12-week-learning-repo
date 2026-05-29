# CourseDB-AI — Demo Script (3–5 minutes)

**Week 12: Evaluation, Polish, Portfolio**

> **TODO(learner):** This is a *starter template* for a recorded or live demo.
> Fill in the talking points and the exact commands/clicks you'll perform.
> Delete this note when your script is complete.

---

## 0. Setup (before recording)

- [ ] `docker-compose up -d` (Postgres + pgvector running)
- [ ] `alembic upgrade head` and `python scripts/seed_data.py`
- [ ] Backend running: `uvicorn app.backend.main:app --reload`
- [ ] Frontend running: `streamlit run app/frontend/streamlit_app.py`

## 1. Introduction (~30s)

> **TODO(learner):** One-sentence pitch + what you'll show.

## 2. Problem Demonstration (~30s)

> **TODO(learner):** Show keyword search missing relevant results.

## 3. SQL Search Demo (~30s)

> **TODO(learner):** Run a CRUD/analytics query via the API or UI.

## 4. Analytics Visualization (~30s)

> **TODO(learner):** Show a chart from the analytics dashboard.

## 5. DBMS Internals (~45s)

> **TODO(learner):** Run a simulator, e.g.:
> `python dbms_internals/bplus_tree/bplus_tree.py` or the Wait-For Graph
> deadlock demo, and narrate what's happening.

## 6. Semantic Search Demo (~45s)

> **TODO(learner):** Run a natural-language query through the semantic/hybrid
> search endpoint and show better relevance than keyword search.

## 7. Comparison Results (~30s)

> **TODO(learner):** Show keyword vs semantic relevance side by side
> (reference `docs/evaluation/`).

## 8. What I Learned (~20s)

> **TODO(learner):** Two or three concrete takeaways.

## 9. Future Work (~20s)

> **TODO(learner):** Next steps.
