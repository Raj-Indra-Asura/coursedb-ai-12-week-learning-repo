# Git Workflow for CourseDB-AI Learning Repository

**Purpose**: Maintain clean Git history that reflects your learning journey

---

## 🌿 Branch Strategy

### Main Branches

- **`main`**: Stable, completed work only
  - Merge only at end of each week after review
  - Never commit directly to main

### Weekly Branches

Create a new branch for each week:

```bash
git checkout -b week-01-dbms-foundations
git checkout -b week-02-sql-basics
git checkout -b week-03-er-modeling
git checkout -b week-04-normalization
git checkout -b week-05-fastapi-postgres
git checkout -b week-06-sql-advanced
git checkout -b week-07-indexing
git checkout -b week-08-query-optimization
git checkout -b week-09-transactions
git checkout -b week-10-semantic-search
git checkout -b week-11-integration
git checkout -b week-12-polish
```

### Feature Branches (Optional)

For experiments or large features within a week:

```bash
git checkout -b week-07/bplus-tree-visualizer
git checkout -b week-10/embedding-service
```

---

## 📝 Commit Message Format

### Standard Format

```
<week>: <short description>

<optional detailed explanation>

<optional notes>
```

### Examples of Good Commits

```
week-01: document DBMS foundations in theory notes

Covered data vs information, schema vs instance, and three-level
architecture. Added examples from CourseDB-AI context.
```

```
week-03: add ER diagram for CourseDB-AI

Created Mermaid diagram showing all entities (Course, Topic, Question,
Resource) and their relationships. Documented cardinality decisions.
```

```
week-04: normalize schema to 3NF

- Identified functional dependencies
- Eliminated partial and transitive dependencies
- Created junction tables for M:N relationships
```

```
week-06: implement audit trigger for question updates

Added PostgreSQL trigger that logs all INSERT and UPDATE operations
on questions table to audit_logs table.
```

```
week-07: add B+ tree insertion visualizer

Educational implementation showing node splits during insertion.
Includes tests for keys: 10, 20, 5, 6, 12, 30, 7.
```

```
week-10: generate embeddings for resource chunks

Used sentence-transformers/all-MiniLM-L6-v2 to generate 384-dim
vectors for all resource chunks. Stored in chunk_embeddings table.
```

```
week-12: write semantic search evaluation report

Evaluated 20 test queries. Semantic search outperformed keyword
search in 15/20 cases. Documented failure modes.
```

### Examples of Bad Commits

❌ `update files` - Too vague
❌ `WIP` - Not descriptive
❌ `fix bug` - What bug?
❌ `add code` - What code?
❌ `week 10` - No description

---

## 🔄 Workflow

### Daily Workflow

1. **Start working**:
```bash
git checkout week-XX-topic
git pull origin week-XX-topic
```

2. **Make changes incrementally**

3. **Commit frequently with clear messages**:
```bash
git add <files>
git commit -m "week-XX: clear description"
```

4. **Push to remote**:
```bash
git push origin week-XX-topic
```

### End of Week Workflow

1. **Review your changes**:
```bash
git log --oneline
git diff main
```

2. **Update LEARNING_LOG.md** with commit links

3. **Merge to main**:
```bash
git checkout main
git merge week-XX-topic
git push origin main
```

4. **Tag the week**:
```bash
git tag -a week-XX -m "Completed Week XX: Topic"
git push origin week-XX
```

---

## 📋 Weekly Commit Checklist

Before merging to main, verify:

- [ ] All deliverables completed
- [ ] Theory notes written in own words
- [ ] Exercises solved
- [ ] Implementation working and tested
- [ ] Reflection completed
- [ ] LEARNING_LOG.md updated
- [ ] Commit messages are clear
- [ ] No sensitive data committed (no .env, no credentials)

---

## 🎯 Commit Frequency

**Recommended**: 2-5 commits per day

**Too few**: One giant commit per week
**Too many**: Commit every line change

**Good pattern**:
- Commit after completing a logical unit
- Commit after writing documentation
- Commit after fixing a bug
- Commit after tests pass

---

## 🚫 What NOT to Commit

Add these to `.gitignore`:

```
# Environment
.env
.env.local

# Python
__pycache__/
*.pyc

# Data files (keep structure, not content)
data/raw/*.csv
data/processed/*.json

# IDE
.vscode/
.idea/

# Dependencies
venv/
node_modules/
```

---

## 🔍 Code Review Before Commit

Ask yourself:

1. **Functionality**: Does this code work?
2. **Tests**: Did I test this?
3. **Documentation**: Did I document this?
4. **Understanding**: Can I explain this code?
5. **Quality**: Is this code clean?
6. **Security**: No vulnerabilities? No secrets?

---

## 📊 Using GitHub Issues (Optional)

Create issues for:
- Weekly learning tasks
- Bugs to fix
- Features to implement
- Concepts to review

Example issues:
- "Week 3: Design ER diagram for CourseDB-AI"
- "Week 7: Implement B+ tree visualizer"
- "Week 10: Debug embedding dimension mismatch"

---

## 🎓 Learning-Focused Commits

Your Git history should tell a learning story:

```
week-01: initial exploration of DBMS concepts
week-01: document file system limitations
week-01: build file-based resource store
week-01: complete Week 1 reflection

week-02: create initial SQL schema
week-02: fix foreign key constraint error
week-02: add 20 SQL practice queries
week-02: complete Week 2 reflection

[and so on...]
```

Someone reading your Git history should see:
- Progressive learning
- Incremental improvements
- Mistakes and fixes
- Theory to practice

---

## 💡 Pro Tips

1. **Commit messages are for future you**: Be specific
2. **Small commits are better**: Easier to understand and revert
3. **Don't commit broken code to main**: Keep main stable
4. **Use branches liberally**: Experiment without fear
5. **Write commit messages in present tense**: "add feature" not "added feature"

---

## 🌟 Example Week Flow

```bash
# Monday: Start week 7
git checkout -b week-07-indexing

# Monday evening
git add weeks/week_07_indexing_bplus_tree_hashing/theory_notes.md
git commit -m "week-07: document B+ tree structure and insertion algorithm"
git push origin week-07-indexing

# Wednesday
git add dbms_internals/bplus_tree/bplus_tree.py
git commit -m "week-07: implement B+ tree node and insertion logic"
git push origin week-07-indexing

# Thursday
git add dbms_internals/bplus_tree/tests/test_bplus_tree.py
git commit -m "week-07: add tests for B+ tree insertion and search"
git push origin week-07-indexing

# Friday: Bug fix
git add dbms_internals/bplus_tree/bplus_tree.py
git commit -m "week-07: fix node split bug when inserting into full leaf"
git push origin week-07-indexing

# Saturday: Documentation
git add weeks/week_07_indexing_bplus_tree_hashing/reflection.md
git add LEARNING_LOG.md
git commit -m "week-07: complete reflection and update learning log"
git push origin week-07-indexing

# Sunday: Merge to main
git checkout main
git merge week-07-indexing
git tag -a week-07 -m "Completed Week 7: Indexing, B+ Tree, Hashing"
git push origin main
git push origin week-07
```

---

## 📚 Resources

- **Git Documentation**: https://git-scm.com/doc
- **Conventional Commits**: https://www.conventionalcommits.org/
- **GitHub Flow**: https://guides.github.com/introduction/flow/

---

**Remember**: Your Git history is part of your portfolio. Make it clean, make it tell a story, make it show your learning journey!
