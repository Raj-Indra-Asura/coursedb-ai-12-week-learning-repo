# Week 1: Implementation Plan

## 🎯 Goal
Build a file-based academic resource storage system and experience its limitations firsthand. This hands-on failure will motivate the need for DBMS concepts in subsequent weeks.

---

## 📋 Step-by-Step Implementation

### Step 1: Design the File Structure (Day 1)
**What to do:**
- Create a directory structure for storing academic resources
- Design text files or JSON files to store:
  - Courses (course_id, name, semester, credit)
  - Topics (topic_id, course_id, topic_name, description)
  - Questions (question_id, topic_id, question_text, difficulty, year)
  - Resources (resource_id, title, type, url)

**Why:**
- Understand how data is organized without a DBMS
- Experience the manual effort required for data management

**Expected output:**
```
data/
├── courses.txt
├── topics.txt
├── questions.txt
└── resources.txt
```

**TODO for you:**
- [ ] Create the directory structure
- [ ] Design the file format (CSV, JSON, or custom)
- [ ] Document the format in `mini_project/README.md`

---

### Step 2: Implement Create Operations (Day 2)
**What to do:**
- Write Python functions to add new records to each file
- Handle file I/O (open, write, close)
- Generate unique IDs manually

**Why:**
- Experience the complexity of managing IDs without auto-increment
- Understand file locking issues
- Discover redundancy problems

**Example code structure:**
```python
def add_course(course_id, name, semester, credit):
    # TODO: Open courses.txt
    # TODO: Append new course
    # TODO: Handle duplicate IDs
    pass

def add_question(question_id, topic_id, question_text, difficulty, year):
    # TODO: Open questions.txt
    # TODO: Append new question
    # TODO: Validate topic_id exists (hard!)
    pass
```

**TODO for you:**
- [ ] Implement `add_course()`
- [ ] Implement `add_topic()`
- [ ] Implement `add_question()`
- [ ] Test with sample data
- [ ] Document what went wrong

---

### Step 3: Implement Read Operations (Day 3)
**What to do:**
- Write functions to search for records
- Implement filtering (e.g., find all questions by difficulty)
- Implement joins manually (e.g., get question with topic name)

**Why:**
- Experience the inefficiency of linear searches
- Understand the pain of manual joins
- Discover missing data problems

**Example code:**
```python
def find_course_by_id(course_id):
    # TODO: Read all courses
    # TODO: Linear search (O(n))
    pass

def get_questions_by_topic(topic_id):
    # TODO: Read all questions
    # TODO: Filter by topic_id
    # TODO: Manually join with topics.txt to get topic name
    pass
```

**TODO for you:**
- [ ] Implement `find_course_by_id()`
- [ ] Implement `get_questions_by_topic()`
- [ ] Implement `get_questions_by_difficulty()`
- [ ] Measure search time for 100 records
- [ ] Document performance issues

---

### Step 4: Implement Update and Delete (Day 4)
**What to do:**
- Write functions to update existing records
- Write functions to delete records
- Handle referential integrity manually

**Why:**
- Experience data inconsistency problems
- Understand orphaned records
- Discover atomicity issues (what if crash during update?)

**Example code:**
```python
def update_course(course_id, new_name):
    # TODO: Read entire file into memory
    # TODO: Find and update the course
    # TODO: Write entire file back
    # TODO: What if crash happens here?
    pass

def delete_topic(topic_id):
    # TODO: Delete from topics.txt
    # TODO: Manually find and delete related questions (easy to forget!)
    # TODO: Handle orphaned questions
    pass
```

**TODO for you:**
- [ ] Implement `update_course()`
- [ ] Implement `delete_topic()` and manually cascade to questions
- [ ] Intentionally forget to delete related questions
- [ ] Document what went wrong (orphaned records!)

---

### Step 5: Test Concurrent Access (Day 5)
**What to do:**
- Run two instances of your program simultaneously
- Try to add records from both instances
- Observe data corruption or lost updates

**Why:**
- Experience race conditions
- Understand why file locking is insufficient
- Motivate transaction management

**Test scenario:**
```python
# Terminal 1: Add course CS101
# Terminal 2: Add course CS102 at the same time
# Result: One of them might be lost!
```

**TODO for you:**
- [ ] Create `test_concurrent_writes.py`
- [ ] Run two instances simultaneously
- [ ] Document lost updates
- [ ] Reflect on why this happened

---

### Step 6: Compare with DBMS Approach (Day 6)
**What to do:**
- Create a comparison table showing file system vs DBMS
- Document every problem you encountered
- Write a reflection on why DBMS is necessary

**Comparison table:**
| Feature | File System | DBMS |
|---------|-------------|------|
| Data redundancy | High (duplicate data) | Low (normalized) |
| Data consistency | Manual effort | Enforced by constraints |
| Search efficiency | O(n) linear scan | O(log n) with indexes |
| Concurrent access | Race conditions | Transaction isolation |
| Referential integrity | Manual (error-prone) | Foreign key constraints |
| Query complexity | Write code for each query | Declarative SQL |
| Recovery | No rollback | Transaction rollback |

**TODO for you:**
- [ ] Fill in the comparison table with your observations
- [ ] Write 2-3 paragraphs on what you learned
- [ ] List 5 specific problems you encountered
- [ ] Explain why CourseDB-AI needs a DBMS

---

### Step 7: Reflection and Documentation (Day 7)
**What to do:**
- Update `reflection.md` with what you learned
- Document your code in `mini_project/`
- Prepare for Week 2 (SQL Basics)

**Reflection prompts:**
1. What was the most frustrating part of using files?
2. How would you handle 10,000 questions in files?
3. Why is manual referential integrity error-prone?
4. How does this motivate DBMS features?
5. Why is CourseDB-AI not just a file organizer?

**TODO for you:**
- [ ] Complete `reflection.md`
- [ ] Add code comments explaining problems
- [ ] Create a summary document of all issues
- [ ] Commit your work with message: "week-01: complete file-based system with documented failures"

---

## 🎯 Connection to CourseDB-AI

This week's mini-project directly connects to CourseDB-AI by:

1. **Showing why we need a database**: CourseDB-AI stores courses, topics, questions, and resources. Imagine managing these in files!

2. **Motivating normalization**: You'll see duplicate data everywhere. Week 4 will teach you how to eliminate this.

3. **Motivating indexes**: You'll experience slow searches. Week 7 will teach you B+ trees.

4. **Motivating transactions**: You'll see data corruption. Week 9 will teach you ACID properties.

5. **Motivating SQL**: You'll write repetitive search code. Week 2 will show you declarative queries.

---

## ✅ Success Criteria

By the end of this week, you should have:
- [ ] A working file-based system (even if flawed)
- [ ] Documented at least 5 specific problems
- [ ] A comparison table showing file system vs DBMS
- [ ] A reflection on why DBMS is necessary
- [ ] Understanding of CourseDB-AI's data infrastructure needs

---

## 🚨 Common Mistakes to Avoid

1. **Making the file system too complex**: Keep it simple! The goal is to experience failure.
2. **Using SQLite**: That defeats the purpose. Use plain text files or JSON.
3. **Not testing concurrent access**: This is where the real problems appear.
4. **Not documenting problems**: Write down every issue you encounter.
5. **Rushing**: Take time to experience the pain. It will motivate you for the rest of the course.

---

## 📚 Resources

- `theory_notes.md` - Core DBMS concepts
- `exercises.md` - Practice problems
- `mini_project/README.md` - Detailed mini-project requirements
- `mistakes_to_expect.md` - Common misconceptions

---

## 🔗 Next Week Preview

**Week 2: SQL Basics Through Academic Data**
- Create real database tables
- Write SQL queries
- Experience the power of declarative queries
- Compare with your Week 1 file-based system
