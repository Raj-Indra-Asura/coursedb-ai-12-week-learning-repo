# Week 12 (supplement): Semi-structured Data — Theory Notes

## 🧭 Navigation

**[← Back to Week 12 Theory](theory_notes.md)** | **[Week 12 Overview](README.md)**

> The last of four breadth supplements for Week 12. It connects classic XML
> theory to the **JSONB** features you can use *today* in PostgreSQL and
> CourseDB-AI.

---

## Learning objectives

- [x] Describe semi-structured data and how it differs from relational data.
- [x] Explain XML, XPath, and XQuery at a high level.
- [x] Relate these to PostgreSQL's JSON/JSONB support.

## Read these references

- Silberschatz, *Database System Concepts*, "XML" / "Semi-structured Data".
- W3C XPath / XQuery primers.
- PostgreSQL docs: JSON types and functions.

---

## 1. What is semi-structured data?

Data exists on a spectrum:

- **Structured** — fixed schema, rows and columns (a relational table).
- **Unstructured** — no inherent schema (free text, images).
- **Semi-structured** — carries its **own** structure via tags/keys, but the
  schema is **flexible and self-describing**, not fixed in advance.

In semi-structured data the structure is **embedded in the data itself** (every
document declares its own fields), so different records can have **different
shapes**, fields can be **nested**, and new fields can appear without an
`ALTER TABLE`. XML and JSON are the two dominant formats.

| | Relational | Semi-structured |
|---|------------|-----------------|
| Schema | fixed, declared up front | self-describing, per-record |
| Shape | flat tuples | nested trees |
| Evolution | `ALTER TABLE` | just add a key |
| Validation | constraints | optional (XSD / JSON Schema) |

---

## 2. XML

**XML** (eXtensible Markup Language) represents data as a **tree** of nested,
named **elements** with **attributes**:

```xml
<question id="q123" difficulty="medium">
  <text>What is normalization?</text>
  <topic id="4">Normalization</topic>
  <tags>
    <tag>1NF</tag>
    <tag>BCNF</tag>
  </tags>
</question>
```

- **Elements** (`<text>...</text>`) nest to form the tree; **attributes**
  (`id="q123"`) annotate elements.
- **Well-formed** = syntactically valid tree. **Valid** = also conforms to a
  schema (**DTD** or **XML Schema / XSD**).
- Verbose but self-describing and strongly tooled; historically dominant in
  enterprise/document exchange (SOAP, config files, publishing).

---

## 3. XPath

**XPath** is a path language for **navigating** the XML tree and selecting nodes,
much like a filesystem path:

```
/question/text                      -> the <text> element
/question/@difficulty               -> the difficulty attribute ("medium")
/question/tags/tag                  -> all <tag> elements
//tag[. = '1NF']                    -> any <tag> whose text is '1NF'
/question/tags/tag[1]               -> the first tag
```

Key pieces: the **axis/path** (`/` child, `//` descendant, `@` attribute) and
**predicates** in `[...]` that filter nodes by position or value. XPath is the
selection primitive that XQuery and XSLT build on.

---

## 4. XQuery

**XQuery** is to XML what SQL is to tables: a full **query language** that uses
XPath to select and then **transform/construct** results. Its core is the
**FLWOR** expression (For, Let, Where, Order by, Return):

```xquery
for $q in /questions/question
where $q/@difficulty = "medium"
order by $q/topic
return <result>{ $q/text/text() }</result>
```

This reads like SQL's `FROM … WHERE … ORDER BY … SELECT`, but iterates over tree
nodes and **constructs new XML** in the `return` clause.

---

## 5. JSONB analogy

Today, **JSON** has largely displaced XML for semi-structured data, and
PostgreSQL supports it natively — giving you semi-structured flexibility **inside
an ACID relational database**.

### `json` vs `jsonb`

| | `json` | `jsonb` |
|---|--------|---------|
| Storage | exact text copy | parsed **binary** form |
| Preserves whitespace/key order/dupes | yes | no (normalized) |
| Write speed | faster (just stores text) | slightly slower (parses) |
| Read/query speed | slower (re-parses) | **faster** |
| Indexable (GIN) | no | **yes** |

**Use `jsonb`** for almost everything — it's queryable and indexable. Use `json`
only if you must preserve the exact input byte-for-byte.

### Querying JSONB (the XPath/XQuery analogy)

```sql
-- sample column:  meta jsonb
-- {"topic": {"id": 4, "name": "Normalization"}, "tags": ["1NF","BCNF"]}

SELECT meta -> 'topic' ->> 'name'      AS topic_name   -- navigate nested keys
FROM   questions;

SELECT *
FROM   questions
WHERE  meta -> 'topic' ->> 'name' = 'Normalization';   -- filter on nested key

SELECT *
FROM   questions
WHERE  meta @> '{"tags": ["1NF"]}';   -- containment: tags includes "1NF"

-- Make containment/key queries fast:
CREATE INDEX idx_questions_meta ON questions USING GIN (meta);
```

Operator cheat-sheet: `->` (get JSON), `->>` (get as text), `#>` / `#>>` (get by
path), `@>` (contains), `?` (key exists). These are PostgreSQL's equivalent of
XPath navigation and predicates.

---

## When to store JSONB vs normalize

**Use JSONB when** the data is genuinely variable-shape (per-record optional
fields), sparse, externally defined (e.g. a third-party API payload), or rarely
queried by its inner fields.

**Normalize into tables (the default for CourseDB-AI) when** the fields are
well-known, queried/joined often, or need foreign keys and constraints — JSONB
gives up referential integrity and makes joins awkward, re-introducing exactly
the anomalies Week 4 normalization removes.

> Best practice: **normalize the core schema, reach for JSONB at the edges** for
> flexible metadata. That hybrid is why PostgreSQL is often "good enough" without
> a separate document database.

---

## How this connects to CourseDB-AI

- CourseDB-AI's schema is **normalized relational** because its entities
  (course, topic, question, resource) are well-known and heavily joined —
  exactly where tables beat JSONB.
- A natural place to *add* JSONB would be a flexible `metadata` column on
  `resources` (varying fields per resource type) — indexed with GIN for
  containment queries.
- The chunk/embedding pipeline in
  [app/services/](../../app/services/) handles semi-structured text; storing
  per-chunk attributes as JSONB is a realistic extension.

---

## Self-check questions

1. What makes data "semi-structured" rather than structured or unstructured?
2. How does an XPath expression navigate an XML document tree?
3. What is the difference between PostgreSQL `json` and `jsonb`?
4. Which JSONB operators would you use to filter on a nested key?
5. When would you store JSONB rather than normalizing into tables?

### Answers

1. The structure is **embedded in and described by the data itself** (tags/keys)
   rather than fixed in a separate schema. Records can have **different,
   nested** shapes and add fields freely — unlike rigid structured tables or
   schemaless unstructured blobs.
2. It uses a **path of steps along axes** — `/` to a child, `//` to any
   descendant, `@` to an attribute — with optional **predicates** `[...]` that
   filter nodes by position or value, selecting a set of nodes from the tree.
3. `json` stores the **exact input text** (preserving whitespace, key order,
   duplicate keys) and re-parses on every read; `jsonb` stores a **parsed binary**
   form that is normalized, faster to query, and **indexable with GIN** — the
   right default.
4. Navigation/extraction operators `->` and `->>` (and `#>` / `#>>` for paths)
   to reach the nested key, and the containment operator `@>` or existence
   operator `?` for membership filters — e.g. `meta -> 'topic' ->> 'name' = 'X'`
   or `meta @> '{"tags":["1NF"]}'`.
5. When the data is **variable-shape, sparse, externally defined, or seldom
   queried by inner fields**. If fields are well-known, frequently
   queried/joined, or need integrity constraints, **normalize** instead.

---

## Notes

Design a JSONB `metadata` column for one CourseDB-AI table, write one `@>`
containment query against it, and the `CREATE INDEX ... USING GIN` that speeds it
up.

---

## 🧭 Navigation

**[← Object/Object-Relational](theory_notes_oo_object_relational.md)** | **[Back to Week 12 Theory](theory_notes.md)**
