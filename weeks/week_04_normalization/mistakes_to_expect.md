# Week 4: Common Normalization Mistakes

## 🎯 Purpose

Normalization requires systematic thinking and careful analysis. This guide documents common mistakes students make and how to avoid them.

---

## Mistake Category 1: Misunderstanding Anomalies

### ❌ Mistake 1.1: Confusing Anomaly Types

**Wrong understanding:**
"Update anomaly means the table can't be updated."

**Correct understanding:**
Update anomaly means updating ONE fact requires changing MULTIPLE rows, risking inconsistency.

**Example:**
```
questions(q_id, course_code, course_title, q_text)
1, CS201, Database Systems, "What is SQL?"
2, CS201, Database Systems, "Explain joins"
```

If course title changes, must update 2 rows. If we miss one → inconsistency!

---

### ❌ Mistake 1.2: Thinking Anomalies Only Occur in Unnormalized Tables

**Wrong:** "If my table is in 1NF, there are no anomalies."

**Correct:** Anomalies can exist in 1NF, 2NF, and even 3NF tables!

**Example (1NF but has anomalies):**
```
enrollments(student_id, course_id, student_name, course_title, grade)
PK: (student_id, course_id)

Still has:
- Update anomaly: student_name repeated for every enrollment
- Delete anomaly: deleting last enrollment loses student info
```

---

### ❌ Mistake 1.3: Not Recognizing Insert Anomaly

**Problem:** Overlooking situations where you can't insert data without unrelated data.

**Example:**
```
questions(question_id, course_id, course_title, question_text)
```

**Cannot do:** Add course "CS301: Operating Systems" without having a question for it.

**Solution:** Separate courses table!

---

## Mistake Category 2: Functional Dependency Errors

### ❌ Mistake 2.1: Incorrect FD Notation

**Wrong:**
```
student_name → student_id
(thinking: "if I know the name, I can find the ID")
```

**Problem:** Multiple students can have same name! student_name doesn't uniquely determine student_id.

**Correct:**
```
student_id → student_name
(knowing ID uniquely determines name)
```

**Rule:** X → Y means X UNIQUELY determines Y (one X value = one Y value)

---

### ❌ Mistake 2.2: Missing Transitive Dependencies

**Table:**
```
employees(emp_id, dept_id, dept_name, dept_building)
```

**Wrong analysis:**
```
FDs:
emp_id → dept_id, dept_name, dept_building
(Looks like no transitive dependencies!)
```

**Correct analysis:**
```
FDs:
emp_id → dept_id
dept_id → dept_name, dept_building

Transitive:
emp_id → dept_id → dept_name
emp_id → dept_id → dept_building
```

**How to avoid:** Ask "Does this non-key attribute depend on another non-key attribute?"

---

### ❌ Mistake 2.3: Confusing Partial and Transitive

**Partial:** Non-key depends on PART of composite key
- Only relevant for composite keys
- Violates 2NF

**Transitive:** Non-key depends on another non-key
- Can occur with any key type
- Violates 3NF

**Example:**
```
enrollments(student_id, course_id, student_name, grade, dept_id, dept_name)
PK: (student_id, course_id)

student_id → student_name [PARTIAL - violates 2NF]
student_id → dept_id → dept_name [TRANSITIVE - violates 3NF]
```

---

## Mistake Category 3: 1NF Errors

### ❌ Mistake 3.1: Missing Multivalued Attributes

**Table:**
```
employees(emp_id, name, skills)
1, Alice, "Python, SQL, Java"
```

**Wrong:** "This is in 1NF because skills is a single string."

**Correct:** "skills" contains multiple values → violates 1NF (not atomic)

**Fix:**
```
employees(emp_id, name)
employee_skills(emp_id, skill)
1, Python
1, SQL
1, Java
```

---

### ❌ Mistake 3.2: Over-Decomposing in 1NF

**Original:**
```
students(student_id, full_name)
1, "Alice Johnson"
```

**Wrong fix:**
```
students(student_id, first_name, last_name, middle_initial, title, suffix)
```

**Problem:** Over-engineering! Not every attribute needs maximum decomposition.

**Right approach:** Decompose only when needed for queries/analysis.
- If you never query by first_name alone → keep full_name
- If you need to sort by last_name → split it

---

### ❌ Mistake 3.3: Forgetting the Primary Key

**Unnormalized:**
```
courses(course_id, title, topics)
1, DBMS, "SQL, ER Model, Normalization"
```

**Wrong 1NF:**
```
course_topics(course_id, topic)
1, SQL
1, ER Model
1, Normalization
```

**Problem:** What's the primary key? (course_id, topic)? Need both!

**Correct:**
```
course_topics(course_id, topic)
PRIMARY KEY (course_id, topic)
```

---

## Mistake Category 4: 2NF Errors

### ❌ Mistake 4.1: Applying 2NF to Single-Key Tables

**Wrong:** "Let me check 2NF for this table..."
```
employees(emp_id, emp_name, dept_name)
PK: emp_id
```

**Correct:** "2NF only applies to composite keys. This table has single key, so 2NF is automatically satisfied."

**Rule:** 2NF is only relevant for tables with composite primary keys!

---

### ❌ Mistake 4.2: Missing Partial Dependencies

**Table:**
```
order_details(order_id, product_id, customer_name, product_price, quantity)
PK: (order_id, product_id)
```

**Wrong analysis:**
"All attributes depend on the full key → 2NF ✓"

**Correct analysis:**
```
quantity depends on (order_id, product_id) [FULL - OK]
customer_name depends only on order_id [PARTIAL - VIOLATION]
product_price depends only on product_id [PARTIAL - VIOLATION]
```

**How to avoid:** For each non-key attribute, ask: "Does this depend on the ENTIRE key or just part?"

---

### ❌ Mistake 4.3: Incorrect Decomposition

**Wrong decomposition:**
```
Original:
order_details(order_id, product_id, customer_name, product_price, quantity)

Wrong split:
table1(order_id, customer_name, quantity)  [WRONG - quantity needs product_id too!]
table2(product_id, product_price)
```

**Correct decomposition:**
```
orders(order_id, customer_name)
products(product_id, product_price)
order_items(order_id, product_id, quantity)
```

**Rule:** Ensure you can reconstruct original data via JOINs!

---

## Mistake Category 5: 3NF Errors

### ❌ Mistake 5.1: Missing Transitive Dependencies

**Table:**
```
students(student_id, student_name, advisor_id, advisor_name, advisor_office)
```

**Wrong:** "No transitive dependencies!"

**Correct:**
```
student_id → advisor_id → advisor_name
student_id → advisor_id → advisor_office

Transitive dependencies violate 3NF!
```

**How to spot:** Look for non-key attributes that determine other non-key attributes.

---

### ❌ Mistake 5.2: Confusing 3NF with BCNF

**Wrong:** "If it's in 3NF, it's perfectly normalized!"

**Correct:** "3NF eliminates most problems, but BCNF is even stricter."

**Example (3NF but not BCNF):**
```
course_instructor(student_id, course_title, instructor)
instructor → course_title [instructor not a superkey → violates BCNF]
```

---

### ❌ Mistake 5.3: Over-Normalizing

**Overly normalized:**
```
courses(course_id, title)
course_codes(course_id, code)  [Separate table for code?]
course_credits(course_id, credits)  [Separate table for credits?]
```

**Problem:** Too many tables! code and credits are simple properties of course.

**Better:**
```
courses(course_id, code, title, credits)
```

**Rule:** Normalize to eliminate anomalies, not to maximize table count!

---

## Mistake Category 6: BCNF Errors

### ❌ Mistake 6.1: Not Checking All Determinants

**Table:**
```
course_instructor(student_id, course_id, instructor_id)
```

**Wrong:** "All FDs have superkeys as determinants → BCNF ✓"

**Correct:** Check ALL functional dependencies, including:
```
instructor_id → course_id (if each instructor teaches one course)
```

If instructor_id → course_id but instructor_id is not a superkey → BCNF violation!

---

### ❌ Mistake 6.2: Thinking BCNF is Always Necessary

**Wrong:** "Every production database must be in BCNF!"

**Correct:** "BCNF is ideal but not always practical. 3NF is usually sufficient."

**Trade-off:**
- BCNF: Zero anomalies, but may require more tables
- 3NF: Minimal anomalies, easier to work with

---

## Mistake Category 7: Denormalization Errors

### ❌ Mistake 7.1: Denormalizing Too Early

**Wrong:** "JOINs are slow, so I'll denormalize everything!"

**Correct:** "First normalize to 3NF, then denormalize selectively based on measured performance."

**Process:**
1. Start with normalized design
2. Implement and measure performance
3. Identify actual bottlenecks
4. Denormalize only what's necessary

---

### ❌ Mistake 7.2: Denormalizing Without Considering Writes

**Wrong decision:**
```
Store like_count in posts table (denormalized)
Update like_count on every like/unlike
```

**Problem:** If likes/unlikes are frequent, updating like_count becomes expensive!

**Consider:**
- Read frequency vs write frequency
- If writes >> reads, keep normalized
- If reads >> writes, denormalize may help

---

### ❌ Mistake 7.3: Forgetting Consistency Enforcement

**Denormalized design:**
```
questions(question_id, topic_id, course_id, ...)
- course_id is redundant with topic_id
```

**Wrong:** "I'll denormalize and forget about it."

**Correct:** "I must ensure course_id stays consistent with topic's course_id!"

**Solutions:**
- Application-level validation
- Database triggers
- Periodic consistency checks

---

## Mistake Category 8: Process Errors

### ❌ Mistake 8.1: Skipping Steps

**Wrong:** "I'll jump straight to 3NF!"

**Correct:** "Apply normalization step-by-step: 1NF → 2NF → 3NF"

**Why:** Each step builds on the previous. Skipping steps misses violations.

---

### ❌ Mistake 8.2: Not Validating with Queries

**Mistake:** Decompose tables without checking if you can still query the data.

**Fix:** After decomposition, write test queries:
```
Original query: SELECT * FROM big_table WHERE ...

After decomposition: Can I still get the same data via JOINs?
SELECT ... FROM table1 JOIN table2 ON ... WHERE ...
```

---

### ❌ Mistake 8.3: Ignoring Real-World Constraints

**Example:**
```
Requirement: "Students can retake courses"
```

**Wrong primary key:**
```
enrollments(student_id, course_id, grade)
PK: (student_id, course_id)  [Can't retake - PK prevents duplicates!]
```

**Correct:**
```
enrollments(student_id, course_id, semester, grade)
PK: (student_id, course_id, semester)
```

---

## Debugging Checklist

When your normalization doesn't work:

### ✅ FD Analysis:
- [ ] Did I list ALL functional dependencies?
- [ ] Did I identify partial dependencies (composite keys)?
- [ ] Did I identify transitive dependencies (non-key → non-key)?
- [ ] Did I check all determinants for BCNF?

### ✅ Decomposition Check:
- [ ] Can I reconstruct original data via JOINs?
- [ ] Are foreign keys correct?
- [ ] Are primary keys identified?
- [ ] Did I lose any data during decomposition?

### ✅ Normalization Level:
- [ ] 1NF: Atomic values? No repeating groups?
- [ ] 2NF: No partial dependencies?
- [ ] 3NF: No transitive dependencies?
- [ ] BCNF: All determinants are superkeys?

### ✅ Practical Check:
- [ ] Can I still query the data I need?
- [ ] Are anomalies eliminated?
- [ ] Is the design maintainable?
- [ ] Are there intentional denormalizations? Why?

---

## Quick Reference: Common Confusions

**1NF vs 2NF vs 3NF:**
```
1NF: Atomic values (structure)
2NF: No partial dependencies (composite keys)
3NF: No transitive dependencies (non-key → non-key)
```

**Partial vs Transitive:**
```
Partial: Part of key → non-key
Transitive: Non-key → non-key
```

**3NF vs BCNF:**
```
3NF: No transitive dependencies
BCNF: All determinants are superkeys (stricter)
```

---

## Learning from Mistakes

**After completing Week 4:**
1. Review this guide
2. Identify which mistakes you made
3. Understand WHY each was a mistake
4. Document your learnings in reflection.md
5. Apply lessons to Week 5 implementation

**Remember:** Making mistakes is how you learn normalization deeply!

---

**Next:** Complete `checkpoints.md` to track your progress!
