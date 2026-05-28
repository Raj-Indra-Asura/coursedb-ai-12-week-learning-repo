# Week 1: DBMS Foundations + Project Orientation

**Duration**: 7 days
**Status**: 🔄 Ready to Start

---

## 🎯 Why This Week Matters

This week establishes the **conceptual foundation** for everything that follows. You need to understand **why databases exist**, what problems they solve, and how CourseDB-AI fits into the bigger picture of data infrastructure and AI systems.

Without understanding DBMS fundamentals, you'll struggle to:
- Design normalized schemas
- Write efficient queries
- Understand indexing and query optimization
- Appreciate transactions and ACID properties
- Position CourseDB-AI as AI infrastructure

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Define what a DBMS is and explain its purpose
✅ Differentiate between data, information, and database
✅ Explain schema vs instance with examples
✅ Describe the three-level architecture (physical, logical, view)
✅ List limitations of file-based data storage
✅ Explain why CourseDB-AI is data infrastructure, not just a chatbot
✅ Position DBMS knowledge as foundational for AI/ML engineering

---

## 📖 Concepts to Learn

### **1. Data vs Information vs Database**

- **Data**: Raw facts (e.g., "John", 25, "CS")
- **Information**: Processed data with meaning (e.g., "John is a 25-year-old CS student")
- **Database**: Organized collection of interrelated data

### **2. Schema vs Instance**

- **Schema**: Structure/design of database (blueprint)
- **Instance**: Actual data at a point in time (snapshot)
- Analogy: Schema is a class definition, instance is an object

### **3. Three-Level Architecture**

- **Physical Level**: How data is stored on disk (files, blocks, pages)
- **Logical Level**: What data is stored and relationships (tables, columns, keys)
- **View Level**: User-specific views of data (customized perspectives)

### **4. Why Not File Systems?**

Limitations:
- Data redundancy
- Data inconsistency
- Difficulty accessing data
- Integrity problems
- Atomicity problems
- Concurrent access issues
- Security problems

### **5. What is a DBMS?**

A Database Management System provides:
- Data definition (DDL)
- Data manipulation (DML)
- Data retrieval (queries)
- Transaction management
- Concurrency control
- Security and authorization
- Recovery from failures

### **6. CourseDB-AI as Data Infrastructure**

CourseDB-AI is NOT:
❌ A simple chatbot
❌ A file organizer
❌ A search engine wrapper

CourseDB-AI IS:
✅ A data infrastructure project
✅ A hybrid relational + vector database system
✅ A semantic retrieval system
✅ A demonstration of DBMS + AI integration

---

## 🧠 Mental Model

```
File System (Week 1) → SQL Tables (Week 2) → ER Design (Week 3) → Normalization (Week 4)
           ↓
Why it fails → Why we need DBMS → How to design properly → How to avoid anomalies
```

---

## 🛠️ Hands-On Exercises

### **Exercise 1: Data vs Information**

Given these raw data points:
- "Alice", 22, "DBMS", 95
- "Bob", 21, "DBMS", 88

Questions:
1. What is the data?
2. What information can you derive?
3. What additional context is needed?

### **Exercise 2: Schema vs Instance**

Consider a `students` table:
- Schema: students(student_id, name, age, major)
- Instance: [(1, "Alice", 22, "CS"), (2, "Bob", 21, "CS")]

Questions:
1. What happens to the schema when you add a new student?
2. What happens to the instance when you add a new student?
3. Can two databases have the same schema but different instances?

### **Exercise 3: Three-Level Architecture**

For a university database:
- Physical: How is student data stored on disk?
- Logical: What tables/columns exist?
- View: What views might different users (students, professors, admin) need?

### **Exercise 4: File System Limitations**

Design a file-based system to store:
- Courses
- Students
- Enrollments

Identify problems with:
- Redundancy
- Updates
- Queries
- Concurrent access

---

## 💻 Mini Implementation

### **Task**: Build a File-Based Academic Resource Store

**Objective**: Create a Python program that stores academic resources (questions, notes) in dictionaries and lists. Then document why it becomes messy.

**File**: `mini_project/file_based_resource_store.py`

**Requirements**:
1. Store at least 5 questions with metadata (topic, year, difficulty)
2. Store at least 3 resources (notes, textbooks)
3. Implement functions:
   - `add_question()`
   - `get_questions_by_topic()`
   - `get_questions_by_year()`
   - `update_question_difficulty()`
4. Document issues you encounter:
   - Data redundancy
   - Inconsistency risks
   - Search inefficiency
   - No constraints

**Expected Output**:
- Working Python script
- Documentation of limitations
- Comparison with what a DBMS would provide

---

## 🐛 Debugging Exercise

**Scenario**: Your file-based system has a bug. A question's difficulty was updated, but when you query by difficulty, you get inconsistent results.

**Task**:
1. Identify why this happened
2. Explain how a DBMS would prevent this
3. Document the lesson learned

---

## 📝 Documentation Task

### **Create**: `theory_notes.md`

Document:
1. What is a DBMS? (in your own words)
2. Data vs Information vs Database (with examples)
3. Schema vs Instance (with examples from CourseDB-AI)
4. Three-level architecture (with diagram)
5. Why file systems fail for complex data
6. How DBMS solves these problems

### **Create**: `implementation_plan.md`

Outline:
1. Why CourseDB-AI needs a DBMS
2. What data will CourseDB-AI store?
3. What queries will users run?
4. Why semantic search needs a relational foundation
5. How this week's learning connects to Week 2 (SQL)

---

## 🤔 Reflection Questions

Answer these in `reflection.md`:

1. **Before this week**: What did I think a database was?
2. **Now**: How has my understanding changed?
3. **Connection to AI**: How does DBMS knowledge help with AI/ML engineering?
4. **CourseDB-AI**: Why is CourseDB-AI more than a simple search engine?
5. **Challenges**: What concepts were hardest to grasp?
6. **Next steps**: What am I curious to learn in Week 2?

---

## ✅ Deliverables

By the end of Week 1, you should have:

- [ ] `theory_notes.md` - DBMS concepts in your own words
- [ ] `exercises.md` - Solutions to exercises
- [ ] `mini_project/file_based_resource_store.py` - Working Python script
- [ ] `mini_project/limitations_doc.md` - Documentation of file system limitations
- [ ] `implementation_plan.md` - CourseDB-AI connection
- [ ] `reflection.md` - Weekly reflection
- [ ] `mistakes_to_expect.md` - Common misconceptions documented
- [ ] First draft of PROJECT_SPEC.md (in root)

---

## 🧪 Self-Check Quiz

Test your understanding:

1. What is the difference between data and information?
2. What is a schema? What is an instance?
3. Name the three levels of database architecture.
4. Why can't we use files instead of a DBMS?
5. What is a DBMS?
6. Name 3 services a DBMS provides.
7. Is CourseDB-AI a chatbot or data infrastructure? Why?
8. How does relational data enable semantic search?
9. What will we learn in Week 2?
10. Why does this matter for your AI/ML career?

**Passing Score**: 8/10

---

## 🔗 How This Connects to CourseDB-AI

| Week 1 Concept | CourseDB-AI Connection |
|----------------|------------------------|
| **DBMS** | Provides structured storage for academic resources |
| **Schema** | We'll design tables for courses, topics, questions, resources |
| **Instance** | Sample DBMS questions and resources will be our data |
| **Three-Level Architecture** | Users see views, app sees logical tables, PostgreSQL handles physical storage |
| **File System Limitations** | Without DBMS, no constraints, no transactions, no efficient search |
| **Data Infrastructure** | CourseDB-AI is AI-ready data infrastructure, not just an app |

---

## 📅 Week 1 Schedule

| Day | Activity | Time |
|-----|----------|------|
| **Day 1** | Read theory, watch videos, take notes | 2-3 hours |
| **Day 2** | Complete exercises, discuss with AI | 2 hours |
| **Day 3** | Build file-based store mini-project | 2-3 hours |
| **Day 4** | Document limitations, debugging exercise | 2 hours |
| **Day 5** | Write implementation plan for CourseDB-AI | 1-2 hours |
| **Day 6** | Write reflection, complete deliverables | 2 hours |
| **Day 7** | Review, self-check quiz, prepare for Week 2 | 1 hour |

**Total**: ~12-15 hours

---

## 🚀 Next Week Preview

**Week 2: SQL Basics Through Academic Data**

You'll learn:
- DDL and DML
- Creating tables for courses, topics, questions
- INSERT, SELECT, WHERE, ORDER BY
- Aggregates and GROUP BY
- 20 SQL practice exercises

**Connection**: Week 1 explains WHY we need DBMS. Week 2 shows HOW to use SQL.

---

## 📚 Resources

- **Textbook**: Database System Concepts (Silberschatz), Chapter 1
- **Videos**: Search "DBMS introduction" on YouTube
- **Practice**: Write examples by hand before coding

---

## 🎓 Learning Tips

1. **Don't rush**: Understanding is more important than speed
2. **Use AI wisely**: Ask for explanations, not just code
3. **Write in your own words**: Don't copy-paste notes
4. **Try to break things**: Intentional failures teach best
5. **Connect to career**: Every concept matters for AI/ML

---

**Ready to start? Open `theory_notes.md` and begin documenting concepts!**

🎯 **Goal**: By Friday, you should be able to explain to a friend why we need databases and why CourseDB-AI is AI infrastructure.
