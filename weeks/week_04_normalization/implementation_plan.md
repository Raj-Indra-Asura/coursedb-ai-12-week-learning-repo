# Week 4: Normalization Implementation Plan

## 📋 7-Day Learning Path

This plan guides you through mastering normalization theory and applying it to CourseDB-AI schema analysis.

---

## Day 1: Data Anomalies + Functional Dependencies

### Morning: Understanding Anomalies (2-3 hours)

**Step 1: Read theory**
- Read `theory_notes.md` - Data anomalies section
- Read `README.md` - Anomaly examples

**Step 2: Identify anomalies in examples**

Practice with this table:
```
courses_instructors(course_id, course_title, credits, instructor_id, instructor_name, instructor_office)
CS201, Database Systems, 3, 501, Dr. Smith, B301
CS201, Database Systems, 3, 502, Dr. Jones, B305
CS202, Data Structures, 3, 501, Dr. Smith, B301
```

**Tasks:**
1. **Update Anomaly**: What happens if Dr. Smith moves to office B310?
   - Answer: Must update 2 rows (CS201 and CS202)
   - Risk: Inconsistency if we miss one

2. **Delete Anomaly**: What happens if we delete Dr. Jones' row?
   - Answer: We lose the fact that Dr. Jones is an instructor

3. **Insert Anomaly**: Can we add a new instructor without assigning a course?
   - Answer: No - we need course_id to insert a row

**Step 3: Practice identifying anomalies**
- Complete Exercise Set 1 in `exercises.md`
- Document each anomaly type
- Understand WHY anomalies are problems

### Afternoon: Functional Dependencies (2-3 hours)

**Step 1: Understand FD notation**

Review these examples:
```
student_id → student_name, email, major
course_id → course_title, credits
(student_id, course_id) → grade
```

**Step 2: Identify FDs in tables**

Practice table:
```
employees(emp_id, emp_name, dept_id, dept_name, dept_building, manager_id, manager_name)
```

List all FDs:
1. emp_id → ?
2. dept_id → ?
3. manager_id → ?
4. Any transitive FDs?

**Step 3: Classify FDs**
- Full vs Partial dependencies
- Transitive dependencies
- Trivial vs Non-trivial

**Step 4: Practice**
- Complete Exercise Set 2 in `exercises.md`
- Create FD diagrams for 3-4 tables
- Identify partial and transitive dependencies

**Deliverable:**
- List of 10+ FD examples with explanations
- Understanding of FD types
- Notes on FD identification process

**Time spent**: _____ hours

---

## Day 2: First Normal Form (1NF)

### Morning: Understanding 1NF (2-3 hours)

**1NF Rules:**
1. Atomic values (no lists or arrays)
2. Same data type per column
3. Unique column names
4. Row order doesn't matter

**Common 1NF Violations:**

**Violation 1: Multivalued attribute**
```
students(student_id, name, phone_numbers)
1, Alice, "555-1234, 555-5678"
```

**Fix:**
```
students(student_id, name)
student_phones(student_id, phone_number)
```

**Violation 2: Repeating groups**
```
courses(course_id, title, topic1, topic2, topic3)
```

**Fix:**
```
courses(course_id, title)
topics(course_id, topic_name)
```

### Afternoon: 1NF Practice (2-3 hours)

**Step 1: Identify 1NF violations**
- Review 5 unnormalized tables
- Spot multivalued attributes
- Spot repeating groups
- Spot non-atomic values

**Step 2: Convert to 1NF**
- Complete Exercise Set 3 in `exercises.md`
- Decompose each table
- Document reasoning

**Step 3: Verify 1NF**
For each converted table, check:
- [ ] All values atomic?
- [ ] No repeating groups?
- [ ] Consistent data types?
- [ ] Can we still query the data?

**Deliverable:**
- 5+ tables converted to 1NF
- Documentation of conversion process
- Notes on common patterns

**Time spent**: _____ hours

---

## Day 3: Second Normal Form (2NF)

### Morning: Understanding 2NF (2-3 hours)

**2NF Rule:** Must be in 1NF + No partial dependencies

**Partial Dependency:** Non-key attribute depends on part of composite key

**Example:**
```
order_details(order_id, product_id, customer_name, product_name, quantity)
PK: (order_id, product_id)

Partial Dependencies:
order_id → customer_name [depends on part of key!]
product_id → product_name [depends on part of key!]
```

**2NF Decomposition:**
```
orders(order_id, customer_name)
products(product_id, product_name)
order_details(order_id, product_id, quantity)
```

**Step 1: Identify composite keys**
- Find tables with composite primary keys
- List all non-key attributes
- Check if each depends on ENTIRE key

**Step 2: Spot partial dependencies**
- For each non-key attribute
- Ask: "Does this depend on the full key or just part?"
- Mark partial dependencies

### Afternoon: 2NF Practice (2-3 hours)

**Step 1: Practice problems**
- Complete Exercise Set 4 in `exercises.md`
- Identify partial dependencies
- Decompose to 2NF

**Step 2: Validate decomposition**
For each decomposition:
- [ ] All tables in 2NF?
- [ ] No partial dependencies remain?
- [ ] Can we reconstruct original data via JOIN?
- [ ] Are foreign keys correct?

**Step 3: Compare with 1NF**
- What improved from 1NF to 2NF?
- What anomalies were eliminated?
- What redundancy was removed?

**Deliverable:**
- 5+ tables normalized to 2NF
- Documentation of partial dependencies
- Notes on 2NF patterns

**Time spent**: _____ hours

---

## Day 4: Third Normal Form (3NF)

### Morning: Understanding 3NF (2-3 hours)

**3NF Rule:** Must be in 2NF + No transitive dependencies

**Transitive Dependency:** Non-key → Non-key (indirect dependency through another attribute)

**Example:**
```
employees(emp_id, emp_name, dept_id, dept_name, dept_building)
PK: emp_id

Transitive:
emp_id → dept_id → dept_name
emp_id → dept_id → dept_building
```

**3NF Decomposition:**
```
employees(emp_id, emp_name, dept_id)
departments(dept_id, dept_name, dept_building)
```

**Step 1: Identify transitive dependencies**
- For each non-key attribute
- Check if it depends on another non-key attribute
- Trace dependency chains (A → B → C)

**Step 2: Understand why transitive is bad**
- Update anomaly: Change dept_name requires updating all employees
- Redundancy: dept_name repeated for every employee in that dept

### Afternoon: 3NF Practice (2-3 hours)

**Step 1: Practice problems**
- Complete Exercise Set 5 in `exercises.md`
- Identify transitive dependencies
- Decompose to 3NF

**Step 2: Multi-step normalization**
Take an unnormalized table through:
1. Unnormalized → 1NF
2. 1NF → 2NF
3. 2NF → 3NF

Document each transformation.

**Step 3: Validate 3NF**
For each table:
- [ ] In 1NF? (atomic values)
- [ ] In 2NF? (no partial dependencies)
- [ ] In 3NF? (no transitive dependencies)
- [ ] All anomalies eliminated?

**Deliverable:**
- 5+ tables normalized to 3NF
- Complete normalization traces
- Notes on 3NF patterns

**Time spent**: _____ hours

---

## Day 5: BCNF + CourseDB-AI Analysis

### Morning: Understanding BCNF (2-3 hours)

**BCNF Rule:** For every FD X → Y, X must be a superkey

**When 3NF is not enough:**
```
course_instructors(student_id, course_title, instructor_name)
PK: (student_id, course_title)

FDs:
(student_id, course_title) → instructor_name [OK]
instructor_name → course_title [VIOLATION!]
```

**Problem:** instructor_name determines course_title, but instructor_name is not a superkey.

**BCNF Decomposition:**
```
student_instructor(student_id, instructor_name)
instructor_course(instructor_name, course_title)
```

**Step 1: Identify BCNF violations**
- List all FDs
- Check if every determinant is a superkey
- Mark violations

**Step 2: Practice BCNF**
- Complete Exercise Set 6 in `exercises.md`
- Find examples where 3NF ≠ BCNF
- Decompose to BCNF

### Afternoon: CourseDB-AI Schema Analysis (2-3 hours)

**Step 1: Analyze each table**

For each table in CourseDB-AI:
- courses(course_id, course_code, title, description, credits)
- topics(topic_id, course_id, topic_name, order_index)
- questions(question_id, course_id, topic_id, question_text, difficulty, marks, year)
- resources(resource_id, course_id, title, resource_type, url)
- resource_chunks(chunk_id, resource_id, chunk_number, chunk_text, embedding)
- users(user_id, username, email, role, created_at)
- search_logs(log_id, user_id, question_id, search_query, timestamp)

**For each table, determine:**
1. Primary key
2. All functional dependencies
3. Normal form (1NF/2NF/3NF/BCNF)
4. Any anomalies?
5. Any intentional denormalization?

**Step 2: Focus on questions table**
```
questions(question_id, course_id, topic_id, ...)
```

**Analysis:**
- Is course_id redundant? (Yes - can derive from topic_id)
- Why is it included? (Performance - avoid JOIN)
- What's the trade-off? (Storage vs query speed)
- Is this good design? (Depends on query patterns)

**Step 3: Create comparison document**

| Table | Normal Form | Anomalies | Design Notes |
|-------|-------------|-----------|--------------|
| courses | 3NF/BCNF | None | Fully normalized |
| questions | 2NF | None (enforced by app) | Intentional denorm |

**Deliverable:**
- Complete CourseDB-AI normalization analysis
- Comparison document
- Notes on design decisions

**Time spent**: _____ hours

---

## Day 6: Denormalization Trade-offs

### Morning: When to Denormalize (2-3 hours)

**Scenarios for denormalization:**

**Scenario 1: Frequent JOIN queries**
```
Normalized:
SELECT q.*, c.title
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
JOIN courses c ON t.course_id = c.course_id

Denormalized:
SELECT * FROM questions WHERE course_id = ?
```

**Trade-off:**
- ✅ Faster query (no JOIN)
- ❌ Redundant data
- ❌ Update complexity

**Scenario 2: Read-heavy workload**
- 90% reads, 10% writes
- Denormalization acceptable if reads >> writes

**Scenario 3: Reporting/Analytics**
- Create denormalized views
- Pre-aggregate data
- Trade storage for speed

**Step 1: Identify denormalization opportunities**
For CourseDB-AI, consider:
1. "Get all questions for a course" (current: denormalized)
2. "Count questions per topic" (normalized - OK?)
3. "Most searched questions" (needs aggregation)

**Step 2: Analyze trade-offs**
For each opportunity:
- Query frequency
- Update frequency
- Storage cost
- Maintenance complexity
- Recommendation

### Afternoon: Practice Problems (2-3 hours)

**Complete Exercise Sets 7-8 in `exercises.md`:**
- Real-world schema design
- E-commerce database
- Social media platform
- Blog platform

For each:
1. Create fully normalized schema
2. Identify common queries
3. Propose denormalization strategies
4. Analyze trade-offs
5. Make recommendations

**Deliverable:**
- 3+ real-world schema designs
- Denormalization analysis for each
- Trade-off documentation

**Time spent**: _____ hours

---

## Day 7: Comprehensive Review + Practice

### Morning: Review All Concepts (2-3 hours)

**Step 1: Review checklist**
- [ ] Can identify all three anomalies
- [ ] Can determine functional dependencies
- [ ] Can apply 1NF (eliminate repeating groups)
- [ ] Can apply 2NF (eliminate partial dependencies)
- [ ] Can apply 3NF (eliminate transitive dependencies)
- [ ] Can apply BCNF (all determinants are keys)
- [ ] Understand denormalization trade-offs

**Step 2: Complete self-check quiz**
- Answer all 10 questions in README.md
- Check answers
- Review weak areas

**Step 3: Create normalization reference guide**

Your personal cheat sheet:
```
1NF: Atomic values, no repeating groups
2NF: 1NF + no partial dependencies (composite keys)
3NF: 2NF + no transitive dependencies (non-key → non-key)
BCNF: 3NF + all determinants are superkeys
```

### Afternoon: Challenge Problems (2-3 hours)

**Challenge 1: Normalize complex schema**
Given a real-world messy database:
- Identify all violations
- Apply 1NF → 2NF → 3NF → BCNF
- Document each step
- Validate with queries

**Challenge 2: Design vs Existing**
Compare your Week 3 ER design with Week 4 normalization knowledge:
- Would you change anything?
- Is your design normalized?
- Any intentional denormalization?

**Challenge 3: Production schema critique**
Find an open-source project's database schema:
- Analyze normalization level
- Identify design decisions
- Propose improvements
- Understand trade-offs

**Deliverable:**
- Completed challenge problems
- Normalization reference guide
- Reflection on learning

**Time spent**: _____ hours

---

## Week 4 Deliverables Checklist

Before moving to Week 5, ensure you have:

### **Required Deliverables:**

- [ ] 15+ normalization exercises completed
- [ ] CourseDB-AI schema analysis document
- [ ] Normalization reference guide
- [ ] Reflection on trade-offs
- [ ] Challenge problems completed

### **Knowledge Verification:**

- [ ] Can identify data anomalies
- [ ] Can determine functional dependencies
- [ ] Can apply 1NF, 2NF, 3NF, BCNF
- [ ] Can decompose tables step-by-step
- [ ] Understand denormalization trade-offs
- [ ] Can analyze production schemas

### **Ready for Week 5:**

- [ ] Understand CourseDB-AI schema completely
- [ ] Know why each table is designed as it is
- [ ] Ready to implement schemas in PostgreSQL
- [ ] Ready to map schemas to SQLAlchemy models

---

## Common Pitfalls to Avoid

See `mistakes_to_expect.md` for detailed list.

**Top 3 mistakes:**
1. Skipping 1NF → jumping straight to 3NF
2. Confusing partial vs transitive dependencies
3. Over-normalizing (creating too many tables)

---

**Next Week**: Week 5 - PostgreSQL + FastAPI Foundation - Implement your normalized schemas!
