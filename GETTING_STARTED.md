# Getting Started with CourseDB-AI

Welcome to your 12-week learning journey! 🎓

---

## 🚀 Quick Start

### 1. Read the Documentation

Start by reading these files in order:

1. **README.md** - Project overview, features, roadmap
2. **PROJECT_SPEC.md** - Technical specification
3. **ROADMAP.md** - Detailed 12-week plan
4. **AI_USAGE_RULES.md** - How to use AI as a learning tool
5. **LEARNING_LOG.md** - Where you'll document your journey

### 2. Set Up Your Environment

```bash
# Clone the repository (if not already done)
git clone https://github.com/Raj-Indra-Asura/coursedb-ai-12-week-learning-repo.git
cd coursedb-ai-12-week-learning-repo

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (will be needed in Week 5)
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Week 1

```bash
# Create a branch for Week 1
git checkout -b week-01-dbms-foundations

# Navigate to Week 1 materials
cd weeks/week_01_dbms_foundations

# Read README.md for this week's learning objectives
# Follow the schedule in the README
```

---

## 📅 Weekly Workflow

Each week follows this pattern:

### **Monday-Tuesday: Learn Theory**
- Read textbook chapters
- Watch videos
- Take notes in `theory_notes.md`
- Ask AI to clarify concepts

### **Wednesday-Thursday: Practice & Implement**
- Complete exercises in `exercises.md`
- Build mini-project
- Test and debug
- Document issues

### **Friday: Document & Connect**
- Write `implementation_plan.md`
- Connect concepts to CourseDB-AI
- Review what you learned

### **Saturday: Reflect & Commit**
- Complete `reflection.md`
- Update `LEARNING_LOG.md`
- Commit your work with clear messages
- Prepare for next week

### **Sunday: Review & Merge**
- Self-check quiz
- Review all deliverables
- Merge to main (if week complete)
- Start reading next week's materials

---

## 🎯 Success Metrics

### Weekly Success

You've successfully completed a week if you can:
- [ ] Explain key concepts without notes
- [ ] Complete all exercises independently
- [ ] Implement working mini-project
- [ ] Connect concepts to CourseDB-AI
- [ ] Document what you learned

### Overall Success (Week 12)

You've successfully completed the journey if you can:
- [ ] Design normalized database schemas
- [ ] Write complex SQL queries
- [ ] Explain DBMS internals (B+ trees, transactions)
- [ ] Implement semantic search with embeddings
- [ ] Build RESTful APIs with FastAPI
- [ ] Integrate PostgreSQL with Python
- [ ] Test database-backed applications
- [ ] Present CourseDB-AI as portfolio project

---

## 🤝 How to Use AI Tools

### Good AI Usage ✅

**For Learning**:
- "Explain functional dependencies with an example"
- "Why is 2NF different from 3NF?"
- "How do B+ trees handle node splits?"

**For Debugging**:
- "I'm getting this error: [error message]. Here's my code: [code]. What's wrong?"
- "Why isn't my foreign key constraint working?"

**For Code Review**:
- "Review my schema design and suggest improvements"
- "Is this query efficient? How can I optimize it?"

### Bad AI Usage ❌

**Don't Ask**:
- "Do all my homework"
- "Generate complete CourseDB-AI code"
- "Write my reflection"

**Remember**: AI is your mentor, not your replacement.

See **AI_USAGE_RULES.md** for detailed guidelines.

---

## 📚 Learning Resources

### Essential Reading

- **Database System Concepts** (Silberschatz, Korth, Sudarshan)
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

### Video Courses

- Search "DBMS fundamentals" on YouTube
- CMU Database Systems (Fall 2023) on YouTube
- PostgreSQL tutorials

### Practice

- SQL exercises on LeetCode
- PostgreSQL tutorial on PostgresTutorial.com
- Practice writing queries by hand first

---

## 🔧 Tools You'll Use

| Tool | Purpose | Week Introduced |
|------|---------|-----------------|
| **Python** | Programming language | Week 1 |
| **PostgreSQL** | Relational database | Week 5 |
| **Docker** | Database containerization | Week 5 |
| **FastAPI** | Backend API framework | Week 5 |
| **SQLAlchemy** | Python ORM | Week 5 |
| **Alembic** | Database migrations | Week 6 |
| **pgvector** | Vector similarity search | Week 10 |
| **Sentence Transformers** | Text embeddings | Week 10 |
| **Streamlit** | Frontend UI | Week 11 |
| **pytest** | Testing framework | Week 5+ |
| **Git** | Version control | Week 1+ |

---

## 🎓 Learning Tips

### 1. Don't Rush
Understanding > Speed. Take time to grasp concepts.

### 2. Write Everything in Your Own Words
Don't copy-paste notes. Rewrite to prove understanding.

### 3. Build, Break, Fix
Intentionally break your code to learn failure modes.

### 4. Test Everything
Write tests before trusting code.

### 5. Reflect Weekly
Document what you learned, what broke, how you fixed it.

### 6. Connect to Career
Link every concept to AI/ML engineering.

### 7. Ask Questions
No question is too basic. Use AI as a patient tutor.

### 8. Commit Frequently
Git history shows your learning journey.

---

## ❓ Common Questions

### "Can I skip weeks?"
No. Each week builds on previous weeks. Follow the sequence.

### "What if I'm stuck?"
1. Read the theory again
2. Ask AI to explain differently
3. Work through examples by hand
4. Take a break and return fresh
5. Document what's confusing

### "How much time per week?"
Plan for 10-15 hours per week. Adjust based on your schedule.

### "Can I go faster?"
Yes, but don't skip exercises or reflections. Understanding matters more than speed.

### "What if I fall behind?"
It's okay! Learning takes time. Catch up before moving to next month.

---

## 🎉 Milestones

### Month 1 Complete
- [ ] Understand DBMS fundamentals
- [ ] Write SQL queries confidently
- [ ] Design normalized schemas
- [ ] Avoid common database design pitfalls

### Month 2 Complete
- [ ] Build FastAPI backend
- [ ] Implement triggers and views
- [ ] Understand indexing deeply
- [ ] Optimize queries with EXPLAIN

### Month 3 Complete
- [ ] Implement semantic search
- [ ] Integrate all components
- [ ] Evaluate system quality
- [ ] Present portfolio project

---

## 💼 Portfolio Preparation

Throughout the journey:
- Keep Git history clean and meaningful
- Document design decisions
- Write honest reflections
- Create evaluation reports
- Prepare demo materials

By Week 12, you'll have:
- Professional README
- Technical case study
- Demo script
- Working application
- GitHub repository showcasing 12-week learning

---

## 🚦 Ready to Start?

1. Read README.md thoroughly
2. Set up your environment
3. Create week-01-dbms-foundations branch
4. Open `weeks/week_01_dbms_foundations/README.md`
5. Begin your learning journey!

---

**Good luck! 🎓 Remember: This is a learning journey, not a race. Understanding and growth matter more than speed.**

**Questions? Stuck? Confused? That's normal! Document it, work through it, learn from it.**

---

## 📧 Stay Connected

- Document your journey in LEARNING_LOG.md
- Commit regularly with clear messages
- Review your progress weekly
- Celebrate small wins!

**Let's build CourseDB-AI and learn deeply! 🚀**
