# AI Usage Rules: Learning-First Guidelines

**Purpose**: This document defines how I use AI tools (GitHub Copilot, ChatGPT, Claude) as a **mentor and pair programmer**, not as a black-box code generator.

---

## 🎯 Core Philosophy

**AI is my mentor, not my replacement.**

I use AI to:
✅ Explain concepts I don't understand
✅ Generate starter code that I then read, annotate, and modify
✅ Debug errors and suggest fixes
✅ Review my code for improvements
✅ Answer "why" questions
✅ Provide examples and analogies

I do NOT use AI to:
❌ Generate large modules without understanding
❌ Copy code blindly without reading
❌ Skip learning the fundamentals
❌ Avoid debugging by regenerating code
❌ Replace my own thinking and problem-solving

---

## 📋 Before Accepting AI-Generated Code

Before using any AI-generated code, I must answer these questions:

### **1. Understanding Check**
- [ ] What problem does this code solve?
- [ ] What are the inputs and outputs?
- [ ] What assumptions does it make?
- [ ] What edge cases does it handle?
- [ ] What can go wrong?

### **2. Code Reading**
- [ ] I have read every line of the generated code
- [ ] I understand what each function does
- [ ] I understand the control flow
- [ ] I understand the data structures used
- [ ] I can explain this code to someone else

### **3. Documentation**
- [ ] I have added comments to tricky parts
- [ ] I have documented why this approach was chosen
- [ ] I have noted any limitations or assumptions
- [ ] I have added TODO comments for improvements

### **4. Testing**
- [ ] I have written test cases
- [ ] I have tested happy path scenarios
- [ ] I have tested edge cases
- [ ] I have intentionally tried to break the code
- [ ] I understand what each test validates

### **5. Learning**
- [ ] I learned something new from this code
- [ ] I can write similar code on my own now
- [ ] I have updated my notes with new concepts

---

## ✅ Before Committing Code

Before committing code to Git, I must verify:

### **Functionality**
- [ ] Code runs without errors
- [ ] Code produces expected output
- [ ] All tests pass
- [ ] Edge cases are handled

### **Understanding**
- [ ] I can explain every function's purpose
- [ ] I can explain the overall design
- [ ] I can justify technical decisions
- [ ] I know which parts I wrote vs AI-generated

### **Documentation**
- [ ] Code has meaningful comments
- [ ] Complex logic is explained
- [ ] README is updated if needed
- [ ] TODO comments mark incomplete work

### **Quality**
- [ ] No unused code or imports
- [ ] Variable names are meaningful
- [ ] Functions are small and focused
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)

---

## 🏁 Before Calling a Feature Complete

Before marking a feature as done, I must:

### **Implementation**
- [ ] Feature works as specified
- [ ] All acceptance criteria met
- [ ] Error handling implemented
- [ ] Input validation added

### **Testing**
- [ ] Unit tests written and passing
- [ ] Integration tests written (if applicable)
- [ ] Manual testing completed
- [ ] Edge cases tested

### **Documentation**
- [ ] Feature documented in README or docs/
- [ ] API endpoints documented (if applicable)
- [ ] Usage examples provided
- [ ] Limitations noted

### **Learning**
- [ ] I understand how it works
- [ ] I documented what I learned
- [ ] I can debug issues independently
- [ ] I updated LEARNING_LOG.md

---

## 🧪 Intentional Breaking Exercise

For every important module, I must:

1. **Try to break it** with edge cases:
   - Empty inputs
   - Null/None values
   - Extremely large inputs
   - Invalid types
   - SQL injection attempts
   - Concurrent access

2. **Document failure modes**:
   - What breaks?
   - Why does it break?
   - How can I fix it?
   - What did I learn?

3. **Add tests for failures**:
   - Write tests that validate fixes
   - Ensure bugs don't reappear

---

## 📝 Weekly Reflection Requirements

Every week, I must document in `LEARNING_LOG.md`:

### **What I Studied**
- Theory topics covered
- Resources used (videos, articles, docs)
- Key concepts learned

### **What I Built**
- Features implemented
- Code written
- Tests added

### **What Broke**
- Bugs encountered
- Errors faced
- Misconceptions revealed

### **How I Debugged It**
- Debugging process
- Tools used (print statements, debugger, logs)
- How I solved the problem

### **What I Misunderstood**
- Concepts I got wrong initially
- Why I was confused
- How I corrected my understanding

### **What I Can Now Explain**
- Topics I can teach someone else
- Code I fully understand
- Design decisions I can justify

### **What I Need to Review**
- Topics still unclear
- Concepts to revisit
- Skills to practice more

### **Commit Links**
- Links to key commits this week
- Highlights from code reviews

---

## 🤖 AI Interaction Patterns

### **Good Pattern: Explain Then Generate**

**Me**: "Explain how B+ trees handle node splits when a node exceeds max capacity."

**AI**: [Explanation]

**Me**: "Now help me write a Python function that splits a B+ tree node."

**AI**: [Code]

**Me**: [Read code, add comments, write tests, commit]

### **Good Pattern: Starter Code + Customization**

**Me**: "Generate a starter SQLAlchemy model for the 'questions' table."

**AI**: [Generates model]

**Me**: [Read model, add constraints, add validation, add comments, commit]

### **Good Pattern: Debug Together**

**Me**: "I'm getting a foreign key constraint error. Here's my code: [code]. What's wrong?"

**AI**: [Analyzes and suggests fix]

**Me**: [Understand the issue, fix it myself, test it, commit]

### **Bad Pattern: Copy-Paste Without Understanding**

**Me**: "Generate complete FastAPI app with database, API endpoints, and tests."

**AI**: [Generates 500 lines]

**Me**: [Copy-paste, commit without reading] ❌ **NEVER DO THIS**

### **Bad Pattern: Avoid Learning**

**Me**: "I don't understand normalization. Just generate a normalized schema for me."

**AI**: [Generates schema]

**Me**: [Use it without learning] ❌ **NEVER DO THIS**

---

## 📚 AI-Assisted Learning Workflow

### **Step 1: Learn Theory First**
- Read textbooks, watch videos, take notes
- Ask AI to explain confusing concepts
- Ask AI for examples and analogies
- Draw diagrams, create mental models

### **Step 2: Solve Exercises Manually**
- Attempt exercises on paper first
- Solve SQL problems manually
- Design schemas on paper
- Only use AI to check answers

### **Step 3: Implement with AI as Pair Programmer**
- Write pseudocode first
- Ask AI to help with implementation
- Read and annotate AI-generated code
- Modify code to fit my understanding

### **Step 4: Test and Break**
- Write tests yourself first
- Ask AI to suggest additional tests
- Intentionally break your code
- Fix bugs yourself

### **Step 5: Reflect and Document**
- Write what you learned in your own words
- Document design decisions
- Note AI-assisted sections
- Update LEARNING_LOG.md

---

## 🎓 Mandatory Documentation

For every AI-generated function, I must document:

```python
def example_function(param1, param2):
    """
    What this function does: [Describe purpose]

    Args:
        param1: [Describe input]
        param2: [Describe input]

    Returns:
        [Describe output]

    Raises:
        [Describe exceptions]

    AI-Assisted: Yes (GitHub Copilot generated starter code, I modified and tested)

    Learning Notes:
    - [What I learned from this function]
    - [Why this approach was chosen]
    - [Limitations or assumptions]
    """
    # Implementation with inline comments
    pass
```

---

## 🚨 Red Flags: When I'm Using AI Wrong

Stop and reassess if:

❌ I'm committing code I don't fully understand
❌ I'm generating entire modules without reading them
❌ I'm avoiding debugging by regenerating code
❌ I'm not writing tests
❌ I'm not updating documentation
❌ I'm not reflecting on what I learned
❌ I can't explain my code to someone else
❌ I'm skipping exercises and going straight to implementation
❌ I'm using AI to skip learning fundamentals

---

## ✅ Green Flags: When I'm Using AI Right

Keep going if:

✅ I'm using AI to clarify concepts
✅ I'm reading and modifying AI-generated code
✅ I'm writing tests for AI-generated code
✅ I'm documenting what I learned
✅ I can explain my code without reading it
✅ I'm attempting problems manually first
✅ I'm intentionally breaking code to learn failure modes
✅ I'm updating my learning log weekly

---

## 📖 Example: Good AI-Assisted Learning Session

### **Scenario**: Implementing a semantic search endpoint

**Me**: "Explain how pgvector cosine similarity works for semantic search."

**AI**: [Explains cosine similarity, vector indexing, and pgvector syntax]

**Me**: [Takes notes, draws diagrams]

**Me**: "Help me write a SQL query that finds the top-k most similar embeddings."

**AI**: [Generates SQL query]

**Me**: [Reads query, adds comments, tests it in psql]

**Me**: "Now help me wrap this in a FastAPI endpoint."

**AI**: [Generates endpoint]

**Me**: [Reads endpoint, adds error handling, adds input validation, writes tests]

**Me**: [Commits with message: "Add semantic search endpoint (AI-assisted)"]

**Me**: [Updates LEARNING_LOG.md with what I learned about pgvector]

---

## 🎯 Final Reminder

**The goal is not to build CourseDB-AI quickly.**
**The goal is to deeply understand DBMS and AI infrastructure.**

If I finish this project and can't explain:
- Why the schema is normalized
- How B+ trees work
- What ACID means
- How embeddings enable semantic search
- How to debug database issues

**Then I failed, even if the code works.**

---

**Success = Understanding + Working Code + Portfolio-Ready Documentation**

**I commit to learning first, coding second.**

---

## 📝 Signature

By working on this project, I commit to these AI usage rules. I will use AI as a mentor and pair programmer, not as a replacement for my own learning and thinking.

**Signed**: Raj Indra Asura
**Date**: May 2026
**Project**: CourseDB-AI 12-Week Learning Journey
