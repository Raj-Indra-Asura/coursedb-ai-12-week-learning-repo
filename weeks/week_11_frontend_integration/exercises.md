# Week 11: Frontend Integration - Exercises

## 🎯 Exercise Overview

Build Streamlit skills through hands-on practice with CourseDB-AI frontend.

---

## Exercise Set 1: Streamlit Basics

### Exercise 1.1: Hello Streamlit

```python
# Create hello.py
import streamlit as st

st.title("CourseDB-AI")
st.write("My first Streamlit app!")

if st.button("Click me"):
    st.balloons()
```

**Tasks:**
1. Run with `streamlit run hello.py`
2. Add a text input for user name
3. Add a greeting message
4. Add a slider for year selection

---

### Exercise 1.2: Widgets Exploration

Create an app with all widget types:
- Text input, text area
- Select box, multiselect
- Slider, checkbox
- Button (regular and primary)

Display selected values below widgets.

---

## Exercise Set 2: Search Interface

### Exercise 2.1: Basic Search

Build a search page:
```python
import streamlit as st
import requests

st.title("Question Search")

query = st.text_area("Enter question")

if st.button("Search"):
    # Mock search for now
    st.write(f"Searching for: {query}")
    st.success("Found 5 results!")
```

---

### Exercise 2.2: API Integration

Connect to CourseDB-AI backend:

```python
@st.cache_data
def search_api(query):
    response = requests.post(
        "http://localhost:8000/api/search/semantic",
        json={"query": query}
    )
    return response.json()

# Use in app
results = search_api(query)
st.json(results)
```

**Tasks:**
1. Display results in expanders
2. Show similarity scores
3. Add filters (year, difficulty)
4. Handle errors gracefully

---

## Exercise Set 3: Analytics Dashboard

### Exercise 3.1: Basic Dashboard

Create analytics page with:
- 4 KPI metrics (questions, topics, courses, avg marks)
- Bar chart of questions by year
- Pie chart of difficulty distribution

Use `plotly.express` for charts.

---

### Exercise 3.2: Interactive Dashboard

Add interactivity:
- Date range filter
- Course selector
- Update charts based on filters
- Cache analytics data

---

## Exercise Set 4: Multi-Page App

### Exercise 4.1: Create Pages

Structure:
```
frontend/
├── Home.py
└── pages/
    ├── 01_Search.py
    ├── 02_Analytics.py
    └── 03_Admin.py
```

Each page should have:
- Title and description
- Relevant functionality
- Consistent styling

---

## Exercise Set 5: State Management

### Exercise 5.1: Search History

Implement search history:
```python
if 'history' not in st.session_state:
    st.session_state.history = []

# Add to history
if st.button("Search"):
    st.session_state.history.append(query)

# Display history
st.sidebar.subheader("Recent Searches")
for q in st.session_state.history[-5:]:
    if st.sidebar.button(q, key=q):
        st.session_state.query = q
```

---

## Exercise Set 6: Complete Integration

### Exercise 6.1: Full CourseDB-AI Frontend

Build complete frontend with:
- Home page with overview
- Search page with filters
- Analytics dashboard
- Admin page (bonus)

Connect all pages to FastAPI backend.

---

## Challenge Exercises

1. **Advanced Search**: Add semantic + keyword + hybrid toggle
2. **Recommendations**: Show similar questions
3. **Export**: Add download results as CSV
4. **Dark Mode**: Implement theme toggle
5. **Real-time**: Add live search (search as you type)

---

## Summary

After completing exercises:
✅ Can build Streamlit apps  
✅ Can integrate with APIs  
✅ Can create dashboards  
✅ Can manage state  
✅ Built complete CourseDB-AI frontend  
