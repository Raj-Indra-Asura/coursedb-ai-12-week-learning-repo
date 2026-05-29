# Week 1: Progress Checkpoints

## 📋 Daily Checkpoints

Use this file to track your progress throughout the week. Check off items as you complete them.

---

## Day 1: DBMS Foundations & Project Setup
**Date**: ___________

### Theory
- [ ] Read `theory_notes.md` - DBMS basics
- [ ] Read `README.md` - Week overview
- [ ] Understand data vs information vs database
- [ ] Understand schema vs instance
- [ ] Understand three-level architecture

### Exercises
- [ ] Complete Exercise 1: Data vs Information
- [ ] Complete Exercise 2: Schema vs Instance
- [ ] Complete Exercise 3: Three-Level Architecture
- [ ] Complete Exercise 4: File System Limitations

### Mini Project
- [ ] Read `mini_project/README.md`
- [ ] Design file structure for academic resources
- [ ] Create directory structure
- [ ] Document file format (CSV/JSON/custom)

### Reflection
- [ ] Write initial thoughts on why DBMS matters
- [ ] List 3 questions you have about databases

**Time spent**: _____ hours

**What I learned today**:
```
[Write 2-3 sentences]
```

**What confused me**:
```
[Write any confusions]
```

---

## Day 2: Create Operations
**Date**: ___________

### Implementation
- [ ] Implement `add_course()` function
- [ ] Implement `add_topic()` function
- [ ] Implement `add_question()` function
- [ ] Implement `add_resource()` function
- [ ] Test with 5-10 sample records
- [ ] Handle duplicate ID problem

### Problems Encountered
- [ ] Document ID generation issue
- [ ] Document file I/O complexity
- [ ] Document data validation difficulty

**Time spent**: _____ hours

**Problems I encountered**:
```
1.
2.
3.
```

**Code files created**:
- [ ] `mini_project/file_store.py`
- [ ] `mini_project/test_create.py`

---

## Day 3: Read Operations
**Date**: ___________

### Implementation
- [ ] Implement `find_course_by_id()`
- [ ] Implement `find_all_courses()`
- [ ] Implement `get_questions_by_topic()`
- [ ] Implement `get_questions_by_difficulty()`
- [ ] Implement manual join (question + topic name)
- [ ] Measure search performance

### Performance Testing
- [ ] Insert 100 records
- [ ] Measure search time for find_by_id
- [ ] Measure search time for filter by attribute
- [ ] Document O(n) linear scan problem

**Time spent**: _____ hours

**Performance observations**:
```
- Search for 1 record in 100: _____ ms
- Filter by difficulty: _____ ms
- Manual join: _____ ms
```

**Why is this slow?**:
```
[Explain why file system search is O(n)]
```

---

## Day 4: Update & Delete Operations
**Date**: ___________

### Implementation
- [ ] Implement `update_course()`
- [ ] Implement `update_question()`
- [ ] Implement `delete_topic()`
- [ ] Implement `delete_question()`
- [ ] Test cascade delete (delete topic → delete related questions)
- [ ] Intentionally forget cascade to see orphaned records

### Problems Discovered
- [ ] Document orphaned records problem
- [ ] Document update inefficiency (read all + write all)
- [ ] Document no rollback capability
- [ ] Document atomicity issue (crash during update)

**Time spent**: _____ hours

**Critical issue discovered**:
```
[Describe the orphaned records problem you created]
```

**Why manual referential integrity is hard**:
```
[Explain in your own words]
```

---

## Day 5: Concurrent Access Testing
**Date**: ___________

### Testing
- [ ] Create `test_concurrent_writes.py`
- [ ] Run two instances simultaneously
- [ ] Try to add courses from both at same time
- [ ] Observe lost updates or data corruption
- [ ] Document the race condition

### Analysis
- [ ] Explain why file locking is insufficient
- [ ] Explain what transactions would solve
- [ ] Document the specific data corruption you observed

**Time spent**: _____ hours

**What went wrong with concurrent writes?**:
```
[Describe the exact problem you observed]
```

**How would DBMS solve this?**:
```
[Your understanding of transaction isolation]
```

---

## Day 6: Comparison & Analysis
**Date**: ___________

### Documentation
- [ ] Create comparison table: File System vs DBMS
- [ ] List all problems encountered (at least 5)
- [ ] Explain each problem and DBMS solution
- [ ] Connect to CourseDB-AI requirements

### Comparison Table
| Feature | File System (My Experience) | DBMS Solution |
|---------|----------------------------|---------------|
| Data redundancy | [Your observation] | Normalization |
| Search speed | [Your measurement] | Indexes (B+ tree) |
| Concurrent access | [Your problem] | Transactions |
| Referential integrity | [Your failure case] | Foreign keys |
| Data consistency | [Your issue] | Constraints |

**Time spent**: _____ hours

**5 Problems I Encountered**:
1.
2.
3.
4.
5.

---

## Day 7: Reflection & Documentation
**Date**: ___________

### Final Tasks
- [ ] Complete `reflection.md` with all prompts
- [ ] Add comprehensive code comments
- [ ] Create summary document of all issues
- [ ] Update README with findings
- [ ] Commit work: "week-01: complete file-based system with documented failures"

### Self-Assessment
- [ ] I can explain what a DBMS is
- [ ] I can list 5 file system limitations
- [ ] I can explain schema vs instance
- [ ] I can explain three-level architecture
- [ ] I understand why CourseDB-AI needs a DBMS
- [ ] I can explain this week's work in an interview

**Time spent**: _____ hours

**Most important thing I learned**:
```
[Write 3-4 sentences on your biggest insight]
```

**How this connects to AI/ML engineering**:
```
[Explain why data infrastructure matters for AI]
```

---

## 📊 Week 1 Summary

### Total Time
- Theory: _____ hours
- Coding: _____ hours
- Debugging: _____ hours
- Documentation: _____ hours
- **Total**: _____ hours

### Completed Deliverables
- [ ] File-based system implementation
- [ ] Test suite with failures documented
- [ ] Comparison table
- [ ] Reflection document
- [ ] All exercises completed
- [ ] Self-check quiz passed

### Key Takeaways
1.
2.
3.

### Questions for Week 2
1.
2.
3.

---

## 🎯 Readiness for Week 2

Before moving to Week 2, ensure:
- [ ] I understand why file systems are insufficient
- [ ] I've experienced at least 5 specific problems
- [ ] I can explain what a DBMS provides
- [ ] I understand CourseDB-AI's data needs
- [ ] I'm motivated to learn SQL

**Am I ready for Week 2?** ☐ Yes ☐ Need more time

**If not ready, what do I need to review?**:
```
[List specific topics to revisit]
```

---

## 🔗 Links to Week 1 Materials

- [README.md](./README.md) - Week overview
- [theory_notes.md](./theory_notes.md) - Core concepts
- [exercises.md](./exercises.md) - Practice problems
- [implementation_plan.md](./implementation_plan.md) - Step-by-step guide
- [reflection.md](./reflection.md) - Reflection prompts
- [mistakes_to_expect.md](./mistakes_to_expect.md) - Common pitfalls
- [mini_project/](./mini_project/) - Hands-on project

---

**Last updated**: ___________
