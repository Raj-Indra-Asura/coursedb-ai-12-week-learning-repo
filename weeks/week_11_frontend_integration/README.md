# Week 11: Frontend Integration with Streamlit

## 📋 Overview

Week 11 brings CourseDB-AI to life with a user-friendly frontend using **Streamlit**. You'll build interactive pages for searching questions, viewing analytics, and managing course content - all in pure Python!

**What you'll master:**
- Streamlit fundamentals and widgets
- Building multi-page applications
- Connecting frontend to FastAPI backend
- State management and caching
- Creating search interfaces
- Building analytics dashboards
- Responsive layouts and user experience
- Deployment strategies

**Why Streamlit:**
- ✅ Pure Python (no HTML/CSS/JS needed)
- ✅ Fast prototyping
- ✅ Built-in widgets and layouts
- ✅ Auto-refresh on code changes
- ✅ Perfect for data/ML applications

---

## 1. Streamlit Basics

### Installation

```bash
pip install streamlit
```

### Hello World

```python
# app.py
import streamlit as st

st.title("CourseDB-AI 🎓")
st.write("Welcome to semantic question search!")

if st.button("Get Started"):
    st.balloons()
    st.success("Let's build something amazing!")
```

Run with:
```bash
streamlit run app.py
```

### Core Concepts

**1. Everything Reruns:** When user interacts, entire script reruns
**2. State Persists:** Use `st.session_state` to maintain state
**3. Cache Data:** Use `@st.cache_data` to avoid reloading
**4. Sequential Execution:** Code runs top to bottom

---

## 2. Text and Display

### Text Elements

```python
# Headings
st.title("Main Title")           # H1
st.header("Section Header")      # H2
st.subheader("Subsection")       # H3

# Text
st.text("Plain monospace text")
st.markdown("**Bold** and *italic*")
st.caption("Small caption text")

# Code
st.code("""
def hello():
    print("Hello World")
""", language="python")

# LaTeX
st.latex(r"\sum_{i=1}^{n} x_i = x_1 + x_2 + ... + x_n")
```

### Data Display

```python
import pandas as pd

# DataFrames
df = pd.DataFrame({
    'course': ['CS201', 'CS202', 'CS203'],
    'title': ['DBMS', 'Algorithms', 'Networks']
})

st.dataframe(df)  # Interactive
st.table(df)      # Static

# JSON
st.json({"key": "value", "nested": {"a": 1}})

# Metrics
st.metric("Total Questions", 1250, delta="+50")
```

### Charts

```python
# Built-in charts
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)

# Plotly (more powerful)
import plotly.express as px
fig = px.scatter(df, x='year', y='marks')
st.plotly_chart(fig)
```

---

## 3. Input Widgets

### Text Input

```python
# Single line
name = st.text_input("Enter your name", placeholder="John Doe")

# Multi-line
query = st.text_area(
    "Enter your question",
    height=150,
    placeholder="What is database normalization?"
)

# Password
password = st.text_input("Password", type="password")
```

### Selection Widgets

```python
# Select box (dropdown)
difficulty = st.selectbox(
    "Select difficulty",
    ["easy", "medium", "hard"],
    index=1  # Default: medium
)

# Multi-select
topics = st.multiselect(
    "Select topics",
    ["Normalization", "SQL", "Indexing", "Transactions"],
    default=["SQL"]
)

# Radio buttons
search_type = st.radio(
    "Search method",
    ["Semantic", "Keyword", "Hybrid"],
    horizontal=True
)

# Slider
year = st.slider("Select year", 2010, 2024, 2023)

# Range slider
year_range = st.slider("Year range", 2010, 2024, (2020, 2024))

# Checkbox
show_advanced = st.checkbox("Show advanced options")
```

### Buttons

```python
# Regular button
if st.button("Search"):
    st.write("Searching...")

# Primary button (highlighted)
if st.button("Submit", type="primary"):
    st.success("Submitted!")

# Download button
st.download_button(
    label="Download Results",
    data=csv_data,
    file_name="results.csv",
    mime="text/csv"
)
```

### File Upload

```python
uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv", "txt"],
    accept_multiple_files=False
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

---

## 4. Layout and Containers

### Columns

```python
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Questions", 1250)

with col2:
    st.metric("Topics", 45)

with col3:
    st.metric("Courses", 12)

# Different widths
col1, col2 = st.columns([2, 1])  # 2:1 ratio
```

### Sidebar

```python
# Add to sidebar
st.sidebar.title("Filters")
year = st.sidebar.slider("Year", 2010, 2024)
difficulty = st.sidebar.multiselect("Difficulty", ["easy", "medium", "hard"])

# Search button in sidebar
if st.sidebar.button("Apply Filters"):
    st.write(f"Filtering by year: {year}")
```

### Tabs

```python
tab1, tab2, tab3 = st.tabs(["Search", "Analytics", "Admin"])

with tab1:
    st.write("Search interface here")

with tab2:
    st.write("Analytics dashboard here")

with tab3:
    st.write("Admin panel here")
```

### Expander

```python
with st.expander("Show question details"):
    st.write("**Question:** What is normalization?")
    st.write("**Answer:** Process of organizing data...")
    st.write("**Marks:** 10")
```

### Container

```python
container = st.container()
container.write("This is inside the container")
container.button("Click me")
```

---

## 5. State Management

### Session State

```python
# Initialize
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Read
st.write(f"Counter: {st.session_state.counter}")

# Update
if st.button("Increment"):
    st.session_state.counter += 1
    st.rerun()  # Force rerun to show new value

# Store complex data
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Access anywhere in script
results = st.session_state.search_results
```

### Form State

```python
with st.form("search_form"):
    query = st.text_input("Query")
    year = st.slider("Year", 2010, 2024)
    
    # Submit button (only this triggers rerun)
    submitted = st.form_submit_button("Search")
    
    if submitted:
        st.write(f"Searching for: {query} in {year}")
```

---

## 6. Caching

### Cache Data

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_courses():
    """Fetch courses from API (expensive operation)"""
    response = requests.get(f"{API_URL}/api/courses")
    return response.json()

# First call: hits API
courses = load_courses()

# Subsequent calls: uses cache
courses = load_courses()  # Instant!
```

### Cache Resources

```python
@st.cache_resource
def get_embedding_model():
    """Load ML model once (heavy resource)"""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

# Loaded once, shared across all users
model = get_embedding_model()
```

**When to use:**
- `@st.cache_data`: For data (DataFrames, lists, dicts, API responses)
- `@st.cache_resource`: For resources (ML models, DB connections)

---

## 7. Multi-Page Applications

### File Structure

```
app/
├── frontend/
│   ├── Home.py                    # Main entry point
│   └── pages/
│       ├── 01_🔍_Search.py
│       ├── 02_📊_Analytics.py
│       └── 03_⚙️_Admin.py
```

### Home.py (Main Page)

```python
# frontend/Home.py
import streamlit as st

st.set_page_config(
    page_title="CourseDB-AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CourseDB-AI")
st.markdown("""
Welcome to CourseDB-AI - your intelligent database question assistant!

**Features:**
- 🔍 Semantic search for questions
- 📊 Analytics dashboard
- ⚙️ Content management

Select a page from the sidebar to get started.
""")

# Quick stats
col1, col2, col3 = st.columns(3)
col1.metric("Questions", "1,250")
col2.metric("Topics", "45")
col3.metric("Courses", "12")
```

### Search Page

```python
# pages/01_🔍_Search.py
import streamlit as st
import requests

st.title("🔍 Semantic Search")

# Sidebar filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Year Range", 2010, 2024, (2020, 2024))
difficulty = st.sidebar.multiselect(
    "Difficulty",
    ["easy", "medium", "hard"],
    default=["medium", "hard"]
)

# Search interface
query = st.text_area(
    "Enter your question or topic",
    height=100,
    placeholder="e.g., What is database normalization?"
)

search_type = st.radio(
    "Search Method",
    ["Semantic", "Keyword", "Hybrid"],
    horizontal=True
)

if st.button("🔎 Search", type="primary"):
    if not query:
        st.warning("Please enter a search query")
    else:
        with st.spinner("Searching..."):
            # Call API
            response = requests.post(
                f"{API_URL}/api/search/semantic",
                json={
                    "query": query,
                    "search_type": search_type.lower(),
                    "filters": {
                        "year_range": year_range,
                        "difficulty": difficulty
                    }
                }
            )
            
            results = response.json()
            
            # Display results
            st.subheader(f"Found {len(results)} questions")
            
            for i, result in enumerate(results, 1):
                with st.expander(
                    f"{i}. {result['question_text'][:80]}... "
                    f"(Similarity: {result['similarity']:.0%})"
                ):
                    st.markdown(f"**Question:** {result['question_text']}")
                    st.markdown(f"**Course:** {result['course_title']}")
                    st.markdown(f"**Topic:** {result['topic_name']}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"**Year:** {result['year']}")
                    col2.write(f"**Difficulty:** {result['difficulty']}")
                    col3.write(f"**Marks:** {result['marks']}")
                    
                    if st.button(f"Find Similar", key=f"similar_{i}"):
                        st.session_state.query = result['question_text']
                        st.rerun()
```

### Analytics Page

```python
# pages/02_📊_Analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Analytics Dashboard")

@st.cache_data(ttl=3600)
def load_analytics():
    response = requests.get(f"{API_URL}/api/analytics")
    return response.json()

data = load_analytics()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Questions", data["total_questions"])
col2.metric("Topics", data["total_topics"])
col3.metric("Courses", data["total_courses"])
col4.metric("Avg Difficulty", data["avg_difficulty"])

# Charts
st.subheader("Questions by Year")
fig1 = px.bar(data["by_year"], x="year", y="count")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Difficulty Distribution")
fig2 = px.pie(data["by_difficulty"], names="difficulty", values="count")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top Topics")
df = pd.DataFrame(data["top_topics"])
st.dataframe(df, use_container_width=True)
```

---

## 8. API Integration

### Setup

```python
# config.py
import os

API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
```

### Helper Functions

```python
# utils/api.py
import requests
import streamlit as st

def call_api(endpoint, method="GET", **kwargs):
    """Call FastAPI backend"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# Usage
def search_questions(query, search_type="semantic"):
    return call_api(
        "/api/search/semantic",
        method="POST",
        json={"query": query, "search_type": search_type}
    )
```

---

## 9. Best Practices

### Performance

```python
# ✅ DO: Cache expensive operations
@st.cache_data
def load_data():
    return expensive_computation()

# ❌ DON'T: Recompute every time
def load_data():
    return expensive_computation()  # Called on every interaction!
```

### State Management

```python
# ✅ DO: Initialize state
if 'results' not in st.session_state:
    st.session_state.results = []

# ❌ DON'T: Access without checking
results = st.session_state.results  # KeyError if not initialized!
```

### Error Handling

```python
# ✅ DO: Handle errors gracefully
try:
    results = call_api("/api/search")
    if results:
        st.dataframe(results)
    else:
        st.info("No results found")
except Exception as e:
    st.error(f"Error: {e}")

# ❌ DON'T: Let errors crash the app
results = call_api("/api/search")  # Unhandled error!
st.dataframe(results)
```

### User Experience

```python
# ✅ DO: Show loading states
with st.spinner("Loading..."):
    data = expensive_operation()

# ✅ DO: Provide feedback
st.success("Search completed!")
st.info("Try refining your filters")
st.warning("No results found")
st.error("Connection failed")

# ✅ DO: Use placeholders
query = st.text_input(
    "Search query",
    placeholder="Enter your question here..."
)
```

---

## 10. Deployment

### Requirements

```txt
streamlit
requests
pandas
plotly
```

### Run Locally

```bash
streamlit run frontend/Home.py
```

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file: `frontend/Home.py`
5. Deploy!

### Environment Variables

```toml
# .streamlit/secrets.toml
API_URL = "https://your-api.com"
API_KEY = "your-secret-key"
```

Access in code:
```python
API_URL = st.secrets["API_URL"]
```

---

## 11. CourseDB-AI Complete Example

### Project Structure

```
coursedb-ai/
├── app/
│   ├── backend/
│   │   └── main.py
│   └── frontend/
│       ├── Home.py
│       ├── pages/
│       │   ├── 01_🔍_Search.py
│       │   ├── 02_📊_Analytics.py
│       │   └── 03_⚙️_Admin.py
│       └── utils/
│           ├── api.py
│           └── config.py
└── requirements.txt
```

### Running Both

```bash
# Terminal 1: Backend
cd app/backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd app/frontend
streamlit run Home.py
```

---

## 12. Summary

**Key Takeaways:**

1. **Streamlit** makes building data apps easy with pure Python
2. **Widgets** provide rich interactivity without JavaScript
3. **Multi-page apps** organize functionality cleanly
4. **Caching** is essential for performance
5. **State management** maintains user context
6. **API integration** connects to FastAPI backend
7. **Deployment** is simple with Streamlit Cloud

**Next Steps:**
- Complete exercises.md for hands-on practice
- Follow implementation_plan.md for 7-day learning
- Review mistakes_to_expect.md to avoid pitfalls
- Build CourseDB-AI frontend!

**Week 12 Preview:** Evaluation & Portfolio!

---

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Community](https://discuss.streamlit.io)
