<!-- DO NOT auto-fill. This file is a skeleton for the learner.
     Headings + self-check questions only. No explanatory prose. -->

# Week 9 (supplement): Crash Recovery & Logging — Theory Notes

## Learning objectives

- [ ] Explain log-based recovery and why it is needed.
- [ ] Describe write-ahead logging (WAL) and the WAL rule.
- [ ] Explain checkpoints and how they bound recovery work.
- [ ] Distinguish redo vs undo.
- [ ] Give an overview of ARIES.

## Read these references

- Silberschatz, *Database System Concepts*, "Recovery System" chapter.
- PostgreSQL docs: Write-Ahead Logging (WAL).
- ARIES paper (Mohan et al., 1992) — overview sections.

## 1. Why recovery?

> **TODO(learner):** Your notes here.

## 2. Log-based recovery

> **TODO(learner):**

## 3. Write-ahead logging (WAL)

> **TODO(learner):**

## 4. Checkpoints

> **TODO(learner):**

## 5. Redo / Undo

> **TODO(learner):**

## 6. ARIES overview

> **TODO(learner):**

## Self-check questions

1. State the write-ahead logging rule. Why must the log record reach disk before the data page?
2. What information does a checkpoint record contain, and how does it speed up recovery?
3. During recovery, in what order are the redo and undo phases performed, and why?
4. What is a fuzzy checkpoint and what problem does it solve?
5. How does ARIES use the LSN (log sequence number) during the analysis phase?

## Notes

> **TODO(learner):**
