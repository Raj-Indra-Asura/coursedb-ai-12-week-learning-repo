# Week 6 (supplement): Access Control — Theory Notes

## 🧭 Navigation

**[← Back to Week 6 Theory](theory_notes.md)** | **[Week 6 Overview](README.md)**

> The main [theory_notes.md](theory_notes.md) covers views, triggers, and
> constraints. This supplement covers **authorization**: who is allowed to do
> what to which data. It is the only place in the curriculum that teaches
> `GRANT`/`REVOKE`, roles, and row-level security, so work through it fully.

---

## Learning objectives

- [x] Use `GRANT` and `REVOKE` to manage privileges.
- [x] Explain roles and role inheritance in PostgreSQL.
- [x] Describe row-level security (RLS) and when to use it.

## Read these references

- PostgreSQL docs: Database Roles, Privileges, Row Security Policies.
- Silberschatz, *Database System Concepts*, "Authorization".

---

## 0. Why access control?

A database usually holds data for many users and applications. **Authorization**
(distinct from *authentication*, which proves *who* you are) decides *what* an
authenticated principal may do. Good access control follows the **principle of
least privilege**: each role gets exactly the privileges it needs and no more,
so a compromised application account or a buggy query cannot read or destroy
data it never needed.

PostgreSQL enforces authorization at three granularities, from coarse to fine:

1. **Object privileges** — what you may do to a whole table/view/schema
   (`GRANT`/`REVOKE`).
2. **Ownership** — the object's owner (and superusers) bypass privilege checks.
3. **Row-level security** — *which rows* within a table you may see or change.

---

## 1. GRANT / REVOKE

`GRANT` gives privileges on an object to a role; `REVOKE` takes them away.

### Common privileges

| Privilege | Applies to | Allows |
|-----------|-----------|--------|
| `SELECT` | table, view, column | read rows |
| `INSERT` | table, column | add rows |
| `UPDATE` | table, column | modify rows |
| `DELETE` | table | remove rows |
| `TRUNCATE` | table | empty table |
| `REFERENCES` | table, column | create foreign keys pointing at it |
| `USAGE` | schema, sequence | "enter" a schema / use a sequence |
| `EXECUTE` | function | call a function |

### Syntax

```sql
-- Grant read access on one table to a role
GRANT SELECT ON courses TO analyst;

-- Grant several privileges at once
GRANT SELECT, INSERT, UPDATE ON questions TO app_writer;

-- Column-level: analyst may read everything except the 'answer' column
GRANT SELECT (question_id, question_text, difficulty) ON questions TO analyst;

-- All tables in a schema (current ones only)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_role;

-- Future tables too (default privileges)
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO readonly_role;

-- Take it back
REVOKE INSERT ON questions FROM app_writer;
```

### WITH GRANT OPTION (delegation)

By default a grantee **cannot** pass a privilege on to others. `WITH GRANT
OPTION` delegates that authority:

```sql
GRANT SELECT ON courses TO lead_analyst WITH GRANT OPTION;
-- lead_analyst can now run:  GRANT SELECT ON courses TO junior_analyst;
```

Revoking a grant option may cascade: if `lead_analyst`'s grant option is revoked
with `CASCADE`, the privileges they handed to `junior_analyst` are revoked too.

```sql
REVOKE GRANT OPTION FOR SELECT ON courses FROM lead_analyst CASCADE;
```

### PUBLIC

`PUBLIC` is a pseudo-role meaning "every role". Be careful — `GRANT SELECT ON x
TO PUBLIC` opens the table to everyone. By default `PUBLIC` has `USAGE` on the
`public` schema and `EXECUTE` on new functions; tightening these is a common
hardening step.

---

## 2. Roles & role inheritance

In modern PostgreSQL there is **no separate "user" object** — there are only
**roles**. A role that can log in (`LOGIN` attribute) is what we informally call
a "user"; a role used only as a privilege container is what we call a "group".

```sql
-- A login role ("user")
CREATE ROLE alice LOGIN PASSWORD 'secret';

-- A group role ("no login", just holds privileges)
CREATE ROLE readonly NOLOGIN;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

-- Make alice a member of readonly
GRANT readonly TO alice;
```

### Inheritance

Whether membership privileges apply **automatically** depends on the member
role's `INHERIT` attribute:

- `INHERIT` (default): `alice` automatically uses every privilege of every role
  she is a member of — she can `SELECT` immediately.
- `NOINHERIT`: `alice` must explicitly adopt the group with `SET ROLE readonly`
  before its privileges apply. This is useful for privileged groups you want
  members to "step into" deliberately.

```sql
SET ROLE readonly;   -- adopt the group's privileges for this session
RESET ROLE;          -- go back to the original login role
```

### Useful role attributes

| Attribute | Meaning |
|-----------|---------|
| `LOGIN` / `NOLOGIN` | can / cannot connect |
| `SUPERUSER` | bypasses **all** permission checks (use sparingly) |
| `CREATEDB`, `CREATEROLE` | may create databases / roles |
| `INHERIT` / `NOINHERIT` | auto-use vs. must `SET ROLE` |
| `BYPASSRLS` | exempt from row-level security policies |

A typical least-privilege setup for CourseDB-AI:

```sql
CREATE ROLE coursedb_app   LOGIN PASSWORD '...';  -- the FastAPI backend
CREATE ROLE coursedb_ro    NOLOGIN;               -- read-only group
CREATE ROLE coursedb_rw    NOLOGIN;               -- read-write group

GRANT SELECT ON ALL TABLES IN SCHEMA public TO coursedb_ro;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO coursedb_rw;
GRANT coursedb_rw TO coursedb_app;   -- the app inherits read-write
```

---

## 3. Row-level security (RLS)

`GRANT` controls access to *whole tables*. **Row-level security** controls
access to *individual rows* by attaching **policies** — boolean expressions
evaluated per row. This is how multi-tenant apps ensure each tenant sees only
its own data, enforced by the database rather than trusting every query.

### Two steps

```sql
-- 1) Turn RLS on for the table (until a policy matches, access is DENIED)
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;

-- 2) Add policies describing which rows are visible/modifiable
CREATE POLICY owner_can_see
    ON questions
    FOR SELECT
    USING (owner = current_user);
```

- **`USING`** filters which existing rows a command can *see* (SELECT/UPDATE/
  DELETE).
- **`WITH CHECK`** validates rows a command tries to *write* (INSERT/UPDATE), so
  a user cannot insert a row "belonging" to someone else.

```sql
CREATE POLICY owner_can_modify
    ON questions
    FOR ALL
    USING (owner = current_user)        -- can act on own rows
    WITH CHECK (owner = current_user);  -- can only write own rows
```

### Important behaviours

- Enabling RLS **with no policy** denies all access to non-owners — a fail-safe
  default. (The table **owner** is exempt unless you also run `ALTER TABLE ...
  FORCE ROW LEVEL SECURITY`.)
- Roles with the `BYPASSRLS` attribute and superusers ignore policies.
- `FOR` can be `ALL`, `SELECT`, `INSERT`, `UPDATE`, or `DELETE`; multiple
  policies for the same command are combined with **OR** (permissive) or **AND**
  (restrictive).

### When to use RLS

Use RLS for **multi-tenant** or **per-user data isolation** that must hold no
matter which query or application connects (defense in depth). For purely
coarse-grained "this role can/can't touch this table" needs, plain
`GRANT`/`REVOKE` is simpler and faster.

---

## How this connects to CourseDB-AI

- The FastAPI backend should connect as a **least-privilege** role
  (`coursedb_rw`/`coursedb_app` above), **not** as a superuser — a SQL-injection
  bug then cannot drop tables it was never granted.
- If CourseDB-AI grew to host multiple students' private question banks in one
  table, an RLS policy `USING (owner = current_user)` would isolate each
  student's rows at the database layer.
- Column-level `GRANT` lets an analytics role read question metadata without
  ever seeing answer text.

---

## Self-check questions

1. What is the difference between a role and a user in PostgreSQL?
2. How does `WITH GRANT OPTION` change privilege delegation?
3. What does `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` do on its own?
4. Write (in your notes) a policy that lets users see only their own rows.
5. How do `GRANT`ed privileges interact with table ownership?

### Answers

1. There is no separate user object — both are **roles**. A "user" is simply a
   role with the `LOGIN` attribute; a "group" is a role without it. The same
   `CREATE ROLE` command creates either.
2. Without it, a grantee can use a privilege but cannot pass it on. `WITH GRANT
   OPTION` lets the grantee `GRANT` that privilege to other roles; revoking the
   option with `CASCADE` also revokes everything they granted onward.
3. It turns on row-level security for that table. By itself (no policies yet) it
   **denies** access to all rows for non-owner roles — a fail-safe default until
   you add `CREATE POLICY` statements.
4. `CREATE POLICY p ON t FOR ALL USING (owner = current_user) WITH CHECK (owner
   = current_user);` — `USING` restricts visible rows, `WITH CHECK` prevents
   writing rows owned by someone else.
5. The table **owner** (and any superuser) bypasses privilege checks entirely —
   `GRANT`/`REVOKE` are irrelevant to them. For RLS specifically, the owner is
   also exempt unless `FORCE ROW LEVEL SECURITY` is set. Privileges only gate
   **non-owner** roles.

---

## Notes

A good hands-on exercise: create `coursedb_ro` and `coursedb_rw` against your
local CourseDB-AI database, connect as each, and confirm that `coursedb_ro`
gets a permission error on `INSERT` while `coursedb_rw` succeeds.

---

## 🧭 Navigation

**[← Back to Week 6 Theory](theory_notes.md)** | **[Week 6 Overview](README.md)** | **[Next: Week 7 →](../week_07_indexing_bplus/README.md)**
