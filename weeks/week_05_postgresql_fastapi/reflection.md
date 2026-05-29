# Week 5: PostgreSQL + FastAPI - Reflection Prompts

## 🧭 Navigation

**[← Back to Week 5 Overview](README.md)** | **[Next: Week 6 →](../week_06_advanced_sql/README.md)**

---

## 🤔 Purpose of Reflection

Week 5 marks the transition from database theory to backend implementation. These reflections help you process the shift from conceptual design to working code.

---

## Reflection 1: Theory to Practice

### Prompt:
**"You spent 4 weeks learning database theory. Now you're building a real backend. Reflect on this transition."**

**Guiding questions:**
1. How does implementing your ER diagram feel compared to drawing it?
2. What theoretical concepts became clearer through implementation?
3. What theory did you wish you understood better before coding?

**Your reflection:**
```
Most surprising aspect of implementation:


Theory that made more sense after coding:


What I wish I had learned better in Weeks 1-4:


Biggest "aha moment":

```

---

## Reflection 2: SQL vs ORM

### Prompt:
**"You learned SQL in Week 2. Now you're using SQLAlchemy ORM. Reflect on the differences."**

**SQL:**
```sql
SELECT * FROM courses WHERE course_id = 1;
```

**ORM:**
```python
db.query(Course).filter(Course.course_id == 1).first()
```

**Your reflection:**
```
Advantages of ORM:
1.
2.
3.

Disadvantages of ORM:
1.
2.
3.

When I would use raw SQL:


When I would use ORM:


My preference:

```

---

## Reflection 3: Database Connections

### Prompt:
**"Managing database connections and sessions is critical. Reflect on how FastAPI's dependency injection helps."**

**Your reflection:**
```
What dependency injection does:


How get_db() works:


Why we use try/finally:


Common mistakes I made with sessions:


Best practices I learned:

```

---

## Reflection 4: Relationships in Code

### Prompt:
**"You designed relationships in Week 3 (ER diagrams). Now you've implemented them with foreign keys and SQLAlchemy relationships. Reflect on the experience."**

**Your reflection:**
```
Most challenging relationship to implement:


Why it was challenging:


How back_populates works:


Difference between relationship() and ForeignKey():


When to use cascade="all, delete-orphan":

```

---

## Reflection 5: Migrations

### Prompt:
**"Database migrations allow schema changes without losing data. Reflect on why this matters."**

**Your reflection:**
```
Why manual ALTER TABLE is dangerous:


How Alembic migrations help:


Mistake I made with migrations:


How I recovered:


Best practices for migrations:
1.
2.
3.

```

---

## Reflection 6: API Design

### Prompt:
**"You built CRUD endpoints following RESTful conventions. Reflect on API design decisions."**

**Your reflection:**
```
Why use different HTTP methods (GET, POST, PUT, DELETE):


Appropriate status codes:
- 200:
- 201:
- 204:
- 400:
- 404:
- 500:

Query parameters vs path parameters:


Most useful Swagger UI feature:

```

---

## Reflection 7: Validation

### Prompt:
**"Pydantic provides automatic validation. Reflect on data validation importance."**

**Your reflection:**
```
Why validate input:


Example of bad input Pydantic caught:


Difference between validation and authentication:


Where validation happens in the stack:


Custom validators I needed:

```

---

## Reflection 8: Error Handling

### Prompt:
**"Production APIs need robust error handling. Reflect on errors you encountered."**

**Your reflection:**
```
Most common error:


Most confusing error message:


How I debugged it:


Error handling strategy:


What errors should expose to users vs log internally:

```

---

## Reflection 9: Development Workflow

### Prompt:
**"Reflect on your development workflow: code, test, debug, repeat."**

**Your reflection:**
```
My typical development cycle:
1.
2.
3.
4.

Most useful debugging tool:


How Swagger UI changed my workflow:


Time spent coding vs testing:


What I would do differently next time:

```

---

## Reflection 10: Comparing Weeks 1-5

### Prompt:
**"Reflect on your learning journey from Week 1 (file-based storage) to Week 5 (production API)."**

**Your reflection:**
```
Week 1 (File System):
- Difficulty: ___/10
- What I learned:

Week 2 (SQL):
- Difficulty: ___/10
- What I learned:

Week 3 (ER Modeling):
- Difficulty: ___/10
- What I learned:

Week 4 (Normalization):
- Difficulty: ___/10
- What I learned:

Week 5 (FastAPI):
- Difficulty: ___/10
- What I learned:

Most valuable week:


Week that prepared me best for implementation:


If I could redo one week:


My confidence now (1-5): ___/5

```

---

## Meta-Reflection: Skills Gained

**Final prompt:**
**"Week 5 taught you full-stack database skills. Reflect on what you can now build."**

**Your reflection:**
```
What I can build now:
1.
2.
3.

Technologies I'm comfortable with:


Technologies I need more practice:


Real-world project I want to build:


How CourseDB-AI relates to job skills:


Next learning goals:
1.
2.
3.

```

---

**Next Steps:** Complete all deliverables and move to Week 6!

---

## 🧭 Navigation

**[← Back to Week 5 Overview](README.md)** | **[🎉 Start Week 6 →](../week_06_advanced_sql/README.md)**
