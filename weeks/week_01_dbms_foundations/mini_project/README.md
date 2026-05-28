# Week 1 Mini Project: File-Based Academic Resource Store

**Objective**: Build a simple Python program to store academic resources using only dictionaries and lists. Then document why this approach fails and why we need a DBMS.

---

## 📋 Requirements

Build a Python program (`file_based_resource_store.py`) that:

1. **Stores Questions** with metadata:
   - question_id
   - question_text
   - topic
   - academic_year
   - difficulty
   - marks

2. **Stores Resources** with metadata:
   - resource_id
   - title
   - resource_type
   - academic_year

3. **Implements Functions**:
   - `add_question()`
   - `get_questions_by_topic(topic_name)`
   - `get_questions_by_year(year)`
   - `get_questions_by_difficulty(difficulty)`
   - `update_question_difficulty(question_id, new_difficulty)`
   - `delete_question(question_id)`

4. **Sample Data**: At least 5 questions, 3 resources

---

## 🎯 Learning Goals

- Experience the limitations of file-based storage
- Understand why data redundancy is problematic
- See how inconsistency can occur
- Realize the difficulty of complex queries
- Appreciate what DBMS provides

---

## ⚠️ Expected Problems

As you build this, you should encounter:

1. **Data Redundancy**: Storing topic names repeatedly
2. **Inconsistency Risk**: Updating topic name in one place but not another
3. **No Constraints**: Can insert invalid data (negative marks, empty text)
4. **Search Inefficiency**: Linear search through all questions
5. **No Relationships**: Difficult to connect questions to resources
6. **No Transactions**: Can't rollback failed multi-step updates
7. **No Concurrency**: Multiple users would corrupt the data structure

---

## 📝 Deliverable

Create `limitations_doc.md` that documents:

1. **What worked**: Basic CRUD operations
2. **What was hard**: [Your experience]
3. **What broke**: [Bugs you encountered]
4. **Why this fails at scale**: [Your analysis]
5. **How DBMS would solve this**: [Your comparison]

---

## 💡 Starter Code Structure

```python
# file_based_resource_store.py

# In-memory storage (simulating file-based storage)
questions = []
resources = []

def add_question(question_id, question_text, topic, academic_year, difficulty, marks):
    """Add a new question to the store"""
    # TODO: Implement
    pass

def get_questions_by_topic(topic_name):
    """Retrieve all questions for a given topic"""
    # TODO: Implement
    pass

def get_questions_by_year(year):
    """Retrieve all questions for a given academic year"""
    # TODO: Implement
    pass

def update_question_difficulty(question_id, new_difficulty):
    """Update the difficulty of a question"""
    # TODO: Implement
    # PROBLEM: What if question_id doesn't exist?
    # PROBLEM: What if new_difficulty is invalid?
    pass

# Test your implementation
if __name__ == "__main__":
    # Add sample data
    add_question(1, "What is normalization?", "Normalization", "2023", "medium", 5)
    add_question(2, "Explain 3NF", "Normalization", "2023", "hard", 10)
    # ... add more

    # Test queries
    print("Questions about Normalization:")
    print(get_questions_by_topic("Normalization"))

    # Try to break it
    # TODO: What happens if you add duplicate IDs?
    # TODO: What happens if you search for non-existent topic?
    # TODO: What happens if you update a deleted question?
```

---

## 🧪 Testing Scenarios

Try to break your system:

1. **Add duplicate question IDs** - What happens?
2. **Update non-existent question** - What happens?
3. **Search for topic with typo** ("Normaliation" instead of "Normalization") - What happens?
4. **Add question with negative marks** - Does it allow it?
5. **Delete question then try to update it** - What happens?

Document all failures in `limitations_doc.md`.

---

## 📊 Comparison Table

Create a table comparing file-based vs DBMS:

| Feature | File-Based Store | DBMS |
|---------|------------------|------|
| **Constraints** | [Your observation] | [What DBMS provides] |
| **Transactions** | [Your observation] | [What DBMS provides] |
| **Concurrency** | [Your observation] | [What DBMS provides] |
| **Queries** | [Your observation] | [What DBMS provides] |
| **Data Integrity** | [Your observation] | [What DBMS provides] |

---

## ✅ Checklist

- [ ] Implemented all required functions
- [ ] Added at least 5 sample questions
- [ ] Tested all query functions
- [ ] Intentionally tried to break the system
- [ ] Documented all failures and limitations
- [ ] Created comparison with DBMS
- [ ] Reflected on why DBMS is necessary

---

## 🔗 Connection to CourseDB-AI

This mini-project shows why CourseDB-AI needs a real DBMS:

- **Without DBMS**: Questions stored in dictionaries, no relationships, no constraints, no semantic search
- **With DBMS**: Proper schema, normalized tables, foreign keys, triggers, indexes, pgvector for semantic search

---

**Remember**: The goal is not to build a perfect file-based system. The goal is to experience its limitations firsthand so you understand why databases exist!
