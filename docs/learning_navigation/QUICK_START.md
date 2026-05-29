# Learning Navigation Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Backend
```bash
# Terminal 1: Start database
docker-compose up -d

# Terminal 2: Start API server
cd app/backend
uvicorn main:app --reload
```

### Step 2: Initialize Curriculum
```bash
# Initialize the learning navigation system
curl -X POST http://localhost:8000/learning/initialize
```

### Step 3: Launch Frontend
```bash
# Terminal 3: Start Streamlit
cd app/frontend
streamlit run streamlit_app.py
```

Open browser to `http://localhost:8501` 🎉

---

## 📚 Quick Reference

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/learning/curriculum` | GET | Get all weeks overview |
| `/learning/weeks/{num}` | GET | Get week with navigation |
| `/learning/weeks/{num}/details` | GET | Get detailed week info |
| `/learning/weeks/{num}/status` | PUT | Update week status |
| `/learning/initialize` | POST | Scan and index curriculum |
| `/learning/search` | GET | Search resources |
| `/learning/stats` | GET | Get statistics |

### Week Status Values

- `not_started` - Week not yet begun
- `in_progress` - Currently working on this week
- `completed` - Week finished

### Resource Types

| Type | Icon | Examples |
|------|------|----------|
| documentation | 📄 | README.md, theory_notes.md |
| exercise | ✏️ | exercises.md, checkpoints.md |
| solution | ✅ | solutions.md |
| notebook | 📓 | *.ipynb |
| code | 💻 | *.py, *.sql |
| reflection | 🤔 | reflection.md |

---

## 🎯 Common Tasks

### View Week 5
```bash
curl http://localhost:8000/learning/weeks/5
```

### Mark Week 7 Complete
```bash
curl -X PUT http://localhost:8000/learning/weeks/7/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Search for Exercises
```bash
curl "http://localhost:8000/learning/search?query=exercise&resource_type=exercise"
```

### Get Progress Stats
```bash
curl http://localhost:8000/learning/stats
```

---

## 🔧 Troubleshooting

### "Curriculum not found"
**Fix:** Run initialization
```bash
curl -X POST http://localhost:8000/learning/initialize
```

### "Connection refused"
**Fix:** Start backend
```bash
cd app/backend && uvicorn main:app --reload
```

### "Database error"
**Fix:** Check PostgreSQL
```bash
docker-compose ps
docker-compose up -d
```

---

## 📖 Week Structure

```
weeks/
├── week_01_dbms_foundations/
│   ├── README.md              # Week overview
│   ├── theory_notes.md        # Core concepts
│   ├── exercises.md           # Practice problems
│   ├── implementation_plan.md # Implementation guide
│   ├── checkpoints.md         # Progress checkpoints
│   ├── reflection.md          # Learning reflections
│   └── mini_project/          # Hands-on project
├── week_02_sql_basics/
├── ...
└── week_12_evaluation_portfolio/
```

---

## 🎨 Frontend Features

### Learning Navigation Page
- 📅 View all 12 weeks at a glance
- 🔄 Refresh curriculum from filesystem
- ⬅️➡️ Navigate between weeks
- 📊 Track overall progress
- 📁 Browse resources by type

### Search Resources Page
- 🔍 Search by keywords
- 🎯 Filter by resource type
- 📄 View file paths

### Statistics Page
- 📈 Total weeks and resources
- 📊 Resources by type breakdown
- ✅ Completion statistics

---

## 💡 Pro Tips

1. **Use keyboard shortcuts**: In Streamlit, use `Ctrl+R` to refresh
2. **Bookmark specific weeks**: Navigate to a week and bookmark the URL
3. **API for automation**: Use the API to build custom learning tools
4. **Track your progress**: Update week status as you complete them
5. **Search effectively**: Use specific keywords for better results

---

## 🔗 Related Documentation

- [Full Documentation](./README.md)
- [API Reference](./README.md#api-reference)
- [Database Schema](./README.md#database-schema)
- [Main Project README](../../README.md)
- [Roadmap](../../ROADMAP.md)

---

## 📞 Need Help?

Check the main documentation: `docs/learning_navigation/README.md`
