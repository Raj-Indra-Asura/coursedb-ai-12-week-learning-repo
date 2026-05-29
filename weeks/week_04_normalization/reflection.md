# Week 4: Normalization - Reflection Prompts

## 🧭 Navigation

**[← Back to Week 4 Overview](README.md)** | **[Next: Week 5 →](../week_05_postgresql_fastapi/README.md)**

---

## 🤔 Purpose of Reflection

Normalization is about making design trade-offs between data integrity, storage efficiency, and query performance. These reflections help you think critically about when to normalize and when to denormalize.

---

## Reflection 1: Why Anomalies Matter

### Prompt:
**"You've learned about update, delete, and insert anomalies. Reflect on a real-world scenario where you've experienced data inconsistency."**

**Guiding questions:**
1. Have you ever seen duplicate or inconsistent data in a system you use?
2. What problems did it cause?
3. How could normalization have prevented it?
4. What's the real-world cost of data anomalies?

**Your reflection:**
```
Real-world example I've encountered:


What went wrong:


How normalization would have helped:


Business impact of the anomaly:


What I learned about data integrity:

```

---

## Reflection 2: Functional Dependencies in Real Life

### Prompt:
**"Functional dependencies (FDs) describe how data relates. Reflect on FDs you encounter in daily life outside of databases."**

**Examples:**
- Social Security Number → Person's Name, DOB
- ISBN → Book Title, Author
- Email Address → Account Owner

**Your reflection:**
```
3 real-world functional dependencies:
1. _____ → _____
2. _____ → _____
3. _____ → _____

Why these relationships matter:


What happens when FDs are violated:


Connection to database design:

```

---

## Reflection 3: The Normalization Process

### Prompt:
**"Reflect on your experience normalizing tables from unnormalized → 1NF → 2NF → 3NF."**

**Guiding questions:**
1. Which step was hardest? Why?
2. Did you ever feel normalization went "too far"?
3. What patterns did you notice in decomposition?

**Your reflection:**
```
Easiest normalization step:


Hardest normalization step:


Why it was hard:


Aha moment during normalization:


Pattern I noticed:


When normalization felt excessive:

```

---

## Reflection 4: 2NF - Partial Dependencies

### Prompt:
**"2NF eliminates partial dependencies in composite-key tables. Reflect on why this matters."**

**Example:**
```
enrollments(student_id, course_id, student_name, course_title, grade)
student_name depends only on student_id (partial!)
course_title depends only on course_id (partial!)
```

**Your reflection:**
```
Why partial dependencies are problematic:


Real-world analogy:


How decomposition helps:


Trade-off of 2NF decomposition:
- Benefit:
- Cost:


When partial dependencies might be acceptable:

```

---

## Reflection 5: 3NF - Transitive Dependencies

### Prompt:
**"3NF eliminates transitive dependencies (non-key → non-key). Reflect on the indirect relationships this creates."**

**Example:**
```
employees(emp_id, dept_id, dept_name)
emp_id → dept_id → dept_name (transitive!)
```

**Your reflection:**
```
Why transitive dependencies cause problems:


My understanding of "indirect" dependencies:


How I identify transitive dependencies:


Real-world example from my exercises:


Most confusing aspect of 3NF:


How I overcame the confusion:

```

---

## Reflection 6: BCNF - The Stricter Rule

### Prompt:
**"BCNF is stricter than 3NF. Reflect on when 3NF is insufficient."**

**Guiding questions:**
1. Did you encounter a table in 3NF but not BCNF?
2. What made it violate BCNF?
3. Is BCNF always necessary?

**Your reflection:**
```
3NF vs BCNF difference:


Example where 3NF wasn't enough:


Why BCNF matters:


When BCNF might be overkill:


My comfort level with BCNF (1-5): ___/5

Areas for improvement:

```

---

## Reflection 7: CourseDB-AI Intentional Denormalization

### Prompt:
**"CourseDB-AI intentionally violates 3NF by storing course_id redundantly in questions table. Reflect on this design decision."**

**Design:**
```
questions(question_id, course_id, topic_id, ...)
- course_id is redundant (derivable from topic_id)
- But included for query performance
```

**Your reflection:**
```
Why course_id is redundant:


Performance benefit of including it:


Storage/consistency cost:


My opinion on this decision:


Alternative designs considered:
1.
2.

If I were the architect, would I make the same choice?


Reasoning:

```

---

## Reflection 8: Performance vs Integrity Trade-off

### Prompt:
**"Normalization improves data integrity but can hurt query performance (more JOINs). Reflect on this fundamental trade-off."**

**Guiding questions:**
1. When should you prioritize integrity over performance?
2. When should you prioritize performance over integrity?
3. How do you make this decision?

**Your reflection:**
```
When integrity is more important:


When performance is more important:


Factors I consider:
1.
2.
3.
4.
5.

Real-world example of each:
- Integrity priority:
- Performance priority:


How I would measure the trade-off:


What I learned about system design:

```

---

## Reflection 9: When to Denormalize

### Prompt:
**"Denormalization deliberately violates normal forms for performance. Reflect on when this is appropriate."**

**Scenarios for denormalization:**
- Read-heavy workloads (90% reads, 10% writes)
- Reporting and analytics
- Caching frequently accessed data
- Avoiding expensive JOINs

**Your reflection:**
```
Denormalization scenarios I identified:
1.
2.
3.

Risks of denormalization:
1.
2.
3.

How to mitigate risks:


Example from my exercises:


Would I denormalize in production?


Under what conditions:

```

---

## Reflection 10: Normalization in Practice

### Prompt:
**"Reflect on how normalization applies beyond academic exercises to real production systems."**

**Guiding questions:**
1. How would you apply normalization in your next project?
2. What questions would you ask when reviewing a schema?
3. How does normalization relate to software architecture?

**Your reflection:**
```
How I'll use normalization skills:


Questions I'll ask when designing schemas:
1.
2.
3.
4.
5.

Connection to software architecture:


Normalization principles that apply beyond databases:


My confidence in schema design (1-5): ___/5

Next steps to improve:

```

---

## Meta-Reflection: Design Thinking

**Final prompt:**
**"Normalization is about systematic thinking - identifying problems and applying rules. Reflect on how this mindset applies beyond database design."**

**Your reflection:**
```
What normalization taught me about design:


Problem-solving patterns I learned:
1.
2.
3.

How this applies to other engineering problems:


Systematic thinking skills gained:


How Week 4 changed my approach to design:

```

---

## Reflection Summary

After completing these reflections, summarize your key takeaways:

**Top 3 Insights:**
1. ___________
2. ___________
3. ___________

**Most Valuable Skill Gained:**
___________

**How Week 4 Prepares Me for Week 5:**
___________

**My Confidence in Normalization (1-5):** _____ / 5

**What I Need to Review:**
___________

---

**Remember:** Normalization is both an art and a science. The rules provide structure, but experience teaches when to break them!

**Next Steps:** Complete all deliverables in `implementation_plan.md` and move to Week 5!

---

## 🧭 Navigation

**[← Back to Week 4 Overview](README.md)** | **[🎉 Start Week 5 →](../week_05_postgresql_fastapi/README.md)**
