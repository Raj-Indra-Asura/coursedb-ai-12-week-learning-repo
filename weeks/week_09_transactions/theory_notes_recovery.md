# Week 9 (supplement): Crash Recovery & Logging — Theory Notes

## 🧭 Navigation

**[← Back to Week 9 Theory](theory_notes.md)** | **[Week 9 Overview](README.md)**

> This supplement completes the **Durability (D)** half of ACID. The main
> [theory_notes.md](theory_notes.md) covers atomicity, isolation, and
> concurrency control. Here we answer the question: *how does a database
> guarantee that a committed transaction survives a crash, and how does it undo
> the effects of one that never committed?*

---

## Learning objectives

- [x] Explain log-based recovery and why it is needed.
- [x] Describe write-ahead logging (WAL) and the WAL rule.
- [x] Explain checkpoints and how they bound recovery work.
- [x] Distinguish redo vs undo.
- [x] Give an overview of ARIES.

## Read these references

- Silberschatz, *Database System Concepts*, "Recovery System" chapter.
- PostgreSQL docs: Write-Ahead Logging (WAL).
- ARIES paper (Mohan et al., 1992) — overview sections.

---

## 1. Why recovery?

A DBMS must keep data **durable** (committed changes survive crashes) and
**atomic** (a crash mid-transaction must not leave half its updates behind).
Two realities make this hard:

1. **Memory is volatile.** Databases work on copies of pages in a memory
   **buffer pool**. A power loss wipes anything not yet written to disk.
2. **Disk writes are not atomic and are buffered/reordered.** A single logical
   commit can touch many pages; a crash can occur after some are flushed and
   others are not.

The failures we recover from:

| Failure type | Example | Handled by |
|--------------|---------|------------|
| Transaction failure | constraint violation, deadlock victim, explicit `ROLLBACK` | undo (logical/page) |
| System crash | power loss, OS panic, process kill | log replay (redo + undo) |
| Media failure | disk corruption | restore from backup + replay archived WAL |

The recovery subsystem's job: after restart, bring the database to a state that
contains **all** committed transactions and **none** of the uncommitted ones.

---

## 2. Log-based recovery

The core idea: **before** changing the database, append a record describing the
change to a sequential, append-only **log** (also called the journal or WAL).
The log is the source of truth for recovery.

### Log record types

```
<T_i, start>                         -- transaction T_i began
<T_i, X, old_value, new_value>       -- T_i updated data item X
<T_i, commit>                        -- T_i committed
<T_i, abort>                         -- T_i aborted
<checkpoint L>                       -- checkpoint; L = list of active txns
```

Each record carries the **before-image** (`old_value`) needed to *undo* and the
**after-image** (`new_value`) needed to *redo*. Logs are written sequentially,
so logging is cheap (one append) compared to random data-page writes.

### Deferred vs immediate modification

- **Deferred modification:** data pages are written only *after* commit. Only
  redo is ever needed (no uncommitted change ever reached disk).
- **Immediate modification:** dirty pages may be written *before* commit. This
  needs **both** undo (for uncommitted txns whose pages leaked to disk) and
  redo (for committed txns whose pages had not yet flushed). Real systems use
  immediate modification with a **steal/no-force** buffer policy (see §6).

---

## 3. Write-ahead logging (WAL)

**The WAL rule:** the log record describing a change must reach **stable
storage** (disk) *before* the corresponding data page is written to disk, and
all of a transaction's log records (including its `commit` record) must be on
disk before the transaction is reported as committed.

```
WAL rule, two parts:
  (1) UNDO rule:  flush log record  BEFORE  flushing the dirty data page.
  (2) REDO rule:  flush the commit log record  BEFORE  acknowledging COMMIT.
```

Why it works:

- If a data page reaches disk early (a "steal"), its **before-image** is already
  in the log, so a crash can be **undone**.
- If a transaction is acknowledged as committed, its **after-images** are
  already in the log, so even if its data pages were still in memory at the
  crash, they can be **redone**.

This is why a `COMMIT` forces a (small, sequential) log flush — `fsync` of the
WAL — but does **not** require flushing the (large, scattered) data pages
immediately. Performance comes from turning many random page writes into one
sequential log write.

### In PostgreSQL

PostgreSQL implements WAL in `pg_wal/`. Relevant knobs:

```sql
SHOW wal_level;            -- minimal | replica | logical
SHOW synchronous_commit;   -- on  => fsync WAL before ack (durable)
                           -- off => faster, small window of loss on crash
SHOW fsync;                -- never turn off in production
```

`synchronous_commit = off` relaxes only the *timing* of the WAL flush (you may
lose the last few committed transactions on a crash) but **never** corrupts the
database — the WAL rule for data pages still holds.

---

## 4. Checkpoints

Without checkpoints, recovery would have to scan the **entire** log from the
beginning of time. A **checkpoint** bounds that work.

At a checkpoint the DBMS:

1. Stops accepting new updates briefly (or uses a fuzzy scheme, below).
2. Flushes all log records in memory to disk.
3. Flushes all **dirty** buffer pages to disk.
4. Writes a `<checkpoint L>` record, where `L` is the set of transactions
   active at checkpoint time.

After a crash, recovery need only go back to the **last checkpoint** (plus
the oldest active transaction recorded there), not to the start of the log.

### Fuzzy checkpoints

A naive checkpoint freezes the whole system while it flushes every dirty page —
unacceptable for a busy database. A **fuzzy checkpoint** writes the checkpoint
record *first* and flushes dirty pages in the background afterward, recording
the position (LSN) up to which all changes are guaranteed on disk. This keeps
the system available during checkpointing. PostgreSQL spreads checkpoint I/O
over time via `checkpoint_completion_target`.

```sql
SHOW checkpoint_timeout;            -- max time between checkpoints
SHOW checkpoint_completion_target;  -- spread I/O over this fraction of the interval
SHOW max_wal_size;                  -- WAL volume that also triggers a checkpoint
```

---

## 5. Redo / Undo

After a crash, recovery replays the log from the last checkpoint:

- **REDO** re-applies the **after-images** of changes so that committed work is
  present on disk. Redo is applied to *all* changes since the checkpoint
  (committed or not) to restore the exact pre-crash page state — this is the
  **repeating history** principle.
- **UNDO** rolls back, using **before-images**, every transaction that did
  **not** commit before the crash (the "losers").

```
Decide winners/losers:
  winner  = has <T, commit>  in the log  -> REDO
  loser   = has <T, start> but no commit -> UNDO

Phase order (classic):
  1. Analysis : scan forward from checkpoint -> find active txns, winners, losers
  2. Redo     : scan forward -> reapply after-images (repeat history)
  3. Undo     : scan backward -> reverse losers using before-images
```

**Idempotency matters:** redo/undo may itself be interrupted by another crash,
so each operation must be safe to apply more than once. This is achieved by
comparing the **LSN stamped on each page** with the LSN of the log record (only
apply if the page is older than the log record).

### Undo must also be logged

When undo reverses a change it writes a **compensation log record (CLR)**
describing the reversal. CLRs are *redo-only* and point past the action they
compensate, so a crash *during* recovery never causes undo to be repeated
endlessly.

---

## 6. ARIES overview

**ARIES** (Algorithms for Recovery and Isolation Exploiting Semantics, Mohan et
al., IBM, 1992) is the recovery method most real systems are based on. Three
principles:

1. **Write-ahead logging** — never write a data page before its log record.
2. **Repeating history during redo** — on restart, redo *everything* since the
   checkpoint (even losers) to reconstruct the exact pre-crash state, *then*
   undo the losers. This simplifies reasoning and supports fine-grained locking.
3. **Logging changes during undo (CLRs)** — so undo is itself crash-safe and
   never repeated.

### Key data structures

| Structure | Purpose |
|-----------|---------|
| **LSN** (Log Sequence Number) | monotonically increasing id of each log record; stamped on each page (`pageLSN`) |
| **Transaction Table** | for each active txn: its `lastLSN` (most recent log record) and status |
| **Dirty Page Table (DPT)** | for each dirty page: its `recLSN` (LSN of the oldest change not yet on disk) |

### The three phases of ARIES

1. **Analysis** — start at the last checkpoint, scan the log forward, and
   reconstruct the Transaction Table and Dirty Page Table as of the crash. The
   smallest `recLSN` in the DPT (the **RedoLSN**) is where redo must begin.
2. **Redo** — from RedoLSN forward, reapply each logged change to a page **only
   if** the page's `pageLSN` is less than the log record's LSN (otherwise the
   change is already on disk). This *repeats history*.
3. **Undo** — scan backward, rolling back all loser transactions, writing a CLR
   for each reversed action and following `prevLSN` chains. CLRs ensure a crash
   mid-undo resumes correctly instead of redoing undone work.

### Buffer policy enabled by ARIES

ARIES supports the most flexible (and fastest) buffer-management policy:

- **STEAL** — a dirty page of an *uncommitted* txn may be written to disk
  (freeing buffer frames). Safe because undo can reverse it (WAL UNDO rule).
- **NO-FORCE** — a *committed* txn's dirty pages need **not** be flushed at
  commit. Safe because redo can reapply them from the WAL (WAL REDO rule).

`STEAL/NO-FORCE` minimizes I/O at commit time but *requires* both undo and redo
— exactly what WAL + ARIES provide.

---

## How this connects to CourseDB-AI

- Every `COMMIT` you issue in the FastAPI backend (e.g. in
  [app/api/courses.py](../../app/api/courses.py)) triggers a WAL flush under
  `synchronous_commit = on`, which is why a server crash never leaves a
  half-inserted course.
- The deadlock victim chosen by the Wait-For Graph demo
  ([dbms_internals/transactions/](../../dbms_internals/transactions/)) is rolled
  back using exactly the undo mechanism described in §5.
- The durability you assert in the Week 9 checkpoints is enforced by §3's WAL
  rule — not by flushing data pages on every write.

---

## Self-check questions

1. State the write-ahead logging rule. Why must the log record reach disk
   before the data page?
2. What information does a checkpoint record contain, and how does it speed up
   recovery?
3. During recovery, in what order are the redo and undo phases performed, and
   why?
4. What is a fuzzy checkpoint and what problem does it solve?
5. How does ARIES use the LSN (log sequence number) during the analysis phase?

### Answers

1. **WAL rule:** a change's log record (with its before-image) must be on stable
   storage before the corresponding data page is written, and the `commit`
   record must be on disk before commit is acknowledged. If a dirty page were
   written before its log record and the system crashed, there would be no
   before-image to undo the (possibly uncommitted) change — the database could
   not be returned to a consistent state.
2. A checkpoint record contains the list of **active transactions** (and, in
   ARIES, the Transaction Table and Dirty Page Table / RedoLSN). It speeds up
   recovery by giving a recent, known starting point: recovery scans only from
   the checkpoint forward instead of from the start of the log.
3. **Redo first, then undo** (repeating-history order). Redo reconstructs the
   exact pre-crash page state for *all* changes since the checkpoint, so the
   database matches what the log describes; only then can undo cleanly reverse
   the loser transactions using consistent before-images. (Classic
   undo-then-redo variants exist, but ARIES uses redo-then-undo.)
4. A **fuzzy checkpoint** writes the checkpoint record immediately and flushes
   dirty pages lazily in the background, recording how far the flush has
   reached. It solves the problem that a naive checkpoint would stall the entire
   system while synchronously flushing every dirty page.
5. During **analysis**, ARIES scans forward from the last checkpoint and uses
   LSNs to rebuild the Transaction Table (`lastLSN` per txn) and Dirty Page
   Table (`recLSN` per page). The minimum `recLSN` (the RedoLSN) tells redo
   where to begin; comparing a page's `pageLSN` to a log record's LSN later
   tells redo whether a change is already on disk.

---

## Notes

Use this space for your own derivations or PostgreSQL experiments. A good
exercise: set `synchronous_commit = off`, run a tight insert loop, `kill -9` the
server, and observe how many of the last committed rows survive — then explain
the result with the WAL rule.

---

## 🧭 Navigation

**[← Back to Week 9 Theory](theory_notes.md)** | **[Week 9 Overview](README.md)** | **[Next: Week 10 →](../week_10_semantic_search/README.md)**
