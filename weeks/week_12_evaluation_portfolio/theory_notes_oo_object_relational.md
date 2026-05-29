# Week 12 (supplement): Object-Oriented & Object-Relational Databases — Theory Notes

## 🧭 Navigation

**[← Back to Week 12 Theory](theory_notes.md)** | **[Week 12 Overview](README.md)**

> One of four breadth supplements for Week 12. This one explains the data models
> that sit *between* pure relational and full NoSQL, and why the SQLAlchemy ORM
> you used in CourseDB-AI exists at all.

---

## Learning objectives

- [x] Describe the object-oriented data model.
- [x] Explain object-relational features (complex types, inheritance).
- [x] Compare OODB / ORDB with the pure relational model.

## Read these references

- Silberschatz, *Database System Concepts*, "Object-Based Databases".
- PostgreSQL docs: composite types, table inheritance, domains.

---

## 0. The impedance mismatch

Application code is written in **object-oriented** languages: objects have
identity, attributes, nested objects, collections, inheritance, and methods. The
relational model offers only **flat tables of scalar values**. Bridging the two
requires constant translation — flattening an object graph into rows on save,
re-assembling rows into objects on load. This friction is the **object-relational
impedance mismatch**, and it is the problem object/object-relational databases
(and ORMs) try to solve.

---

## 1. Object-oriented data model

An **object-oriented database (OODB)** stores **objects directly**, as they
exist in the programming language, with:

- **Object identity (OID):** every object has a unique id independent of its
  attribute values (unlike a relational primary key derived from data).
- **Complex/nested objects:** an attribute can itself be an object or a
  collection — no need to decompose into separate tables.
- **Inheritance & methods:** classes form hierarchies; behaviour can live with
  the data.

- **Strength:** no impedance mismatch — persist/retrieve object graphs directly;
  great for complex, deeply-nested domains (CAD, engineering).
- **Weakness:** weak ad-hoc querying compared to SQL, smaller ecosystems, poor
  interoperability. Pure OODBs (e.g. db4o, ObjectDB, Versant) never reached
  mainstream adoption.

---

## 2. Object-relational features

The mainstream answer was to **extend the relational model** rather than replace
it. An **object-relational database (ORDB)** — PostgreSQL is the classic example
— keeps tables, SQL, and ACID, but adds object-like features:

- **Composite (complex) types** — a column whose value is a structured record.
- **Arrays** — a column holding a collection.
- **User-defined types & domains** — named, constrained types.
- **Type/table inheritance** — tables that inherit columns from a parent.
- **Polymorphic / user-defined functions and operators.**

```sql
-- Composite type: structure inside a column
CREATE TYPE address AS (street text, city text, zip text);

CREATE TABLE instructors (
    id      int PRIMARY KEY,
    name    text,
    office  address,          -- composite-typed column
    courses int[]             -- array column
);

INSERT INTO instructors VALUES
    (1, 'Dr. Smith', ROW('1 Main','Springfield','00001'), ARRAY[201,202]);

SELECT name, (office).city, courses[1] FROM instructors;
```

---

## 3. Inheritance & complex types

PostgreSQL **table inheritance** lets a child table inherit a parent's columns:

```sql
CREATE TABLE resources (
    resource_id int PRIMARY KEY,
    title       text,
    year        int
);

-- video_resources gets all columns of resources, plus its own
CREATE TABLE video_resources (
    duration_min int
) INHERITS (resources);

-- A query on the parent also scans children
SELECT title FROM resources;          -- includes videos
SELECT title FROM ONLY resources;     -- parent rows only
```

**Drawbacks of PostgreSQL table inheritance** (why it's rarely used in
practice):

- **Constraints/indexes are not inherited the way you'd expect** — a primary key
  or `UNIQUE` on the parent is **not** enforced across child tables, so a
  duplicate id can exist in a child.
- Foreign keys pointing at the parent don't see child rows.
- Modern **declarative partitioning** (Week 12 distributed notes) superseded most
  legitimate uses.

For these reasons, complex types/arrays/`JSONB` are preferred over table
inheritance for object-like modeling.

---

## 4. Comparison with the relational model

| Aspect | Pure Relational | Object-Relational (PostgreSQL) | Object-Oriented (OODB) |
|--------|-----------------|--------------------------------|------------------------|
| Unit of storage | flat tuples | tuples + complex types/arrays | objects |
| Identity | primary key (value-based) | primary key | OID (independent) |
| Nesting | none (normalize) | composite types, arrays, JSONB | native |
| Inheritance | none | table inheritance (limited) | first-class |
| Querying | full SQL | full SQL + extensions | weaker, navigational |
| ACID / ecosystem | strong | strong | varies / small |

The relational model wins on **simplicity, querying, and integrity**; ORDB adds
**escape hatches** for object-like data without giving those up; OODB removes the
mismatch entirely but at the cost of querying power and ecosystem.

---

## How this connects to CourseDB-AI

- **ORMs are the everyday face of this topic.** CourseDB-AI's
  [app/db/models.py](../../app/db/models.py) uses **SQLAlchemy** to map Python
  classes ↔ relational tables — an ORM exists precisely to paper over the
  impedance mismatch from §0.
- CourseDB-AI deliberately stays **normalized relational** (Weeks 3–4) for
  integrity and querying, reaching for an object-relational feature (**JSONB**,
  see [semi-structured supplement](theory_notes_semi_structured.md)) only where
  flexible nested data is genuinely needed.
- Knowing inheritance's pitfalls (§3) explains why the schema models `resources`
  with a `type`/discriminator column rather than child tables.

---

## Self-check questions

1. What is the "impedance mismatch" between OO programming and relational
   databases?
2. How does PostgreSQL support composite/complex types?
3. What are the drawbacks of table inheritance in PostgreSQL?
4. When would an object-relational model be preferable to a pure relational one?
5. How do ORMs relate to object-relational concepts?

### Answers

1. It is the friction between the **object world** (identity, nesting,
   collections, inheritance) and the **relational world** (flat tables of
   scalars). Code must constantly flatten objects into rows and reassemble rows
   into objects.
2. Via **composite types** (`CREATE TYPE ... AS (...)`), **array columns**,
   **domains**, and **user-defined types**, letting a single column hold a
   structured record or collection while still being queryable with SQL.
3. Inherited child tables **don't enforce the parent's primary key / unique
   constraints**, foreign keys to the parent don't include child rows, and the
   feature is largely superseded by declarative partitioning — so it's
   error-prone and rarely recommended.
4. When the domain has **complex, nested, or variable-shape data** (arrays,
   structured attributes, occasional schema flexibility) but you still want SQL,
   joins, and ACID — ORDB features (composite types, arrays, JSONB) give that
   without leaving the relational world.
5. **ORMs** (like SQLAlchemy) automate the object-relational mapping: they let
   you work with classes/objects in code while persisting to relational tables,
   operationalizing the same bridge that object-relational *database* features
   provide at the storage layer.

---

## Notes

Pick one CourseDB-AI model class and write, in your notes, both its SQLAlchemy
class and the equivalent `CREATE TABLE` — the two sides of the mapping.

---

## 🧭 Navigation

**[← NoSQL Introduction](theory_notes_nosql_intro.md)** | **[Next supplement: Semi-structured Data →](theory_notes_semi_structured.md)**
