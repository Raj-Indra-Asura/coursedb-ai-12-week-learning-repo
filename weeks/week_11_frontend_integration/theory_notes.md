# Week 11: Frontend Integration with Streamlit - Theory Notes

## 📚 Core Concepts

### 1. What is Streamlit?

**Streamlit**: Open-source Python framework for building data apps quickly.

**Why Streamlit for CourseDB-AI?**
- ✅ Pure Python (no HTML/CSS/JS needed)
- ✅ Fast prototyping
- ✅ Built-in widgets (buttons, sliders, text inputs)
- ✅ Auto-refresh on code changes
- ✅ Great for ML/data apps

**Installation:**
```bash
pip install streamlit
```

**Hello World:**
```python
import streamlit as st

st.title("CourseDB-AI")
st.write("Welcome to semantic question search!")

if st.button("Click me"):
    st.write("Button clicked!")
```

**Run:**
```bash
streamlit run app.py
```

---

### 2. Streamlit Basics

#### **Text Display**
```python
st.title("Main Title")           # Largest heading
st.header("Header")              # Section header
st.subheader("Subheader")        # Subsection
st.text("Plain text")            # Monospace text
st.markdown("**Bold** *italic*") # Markdown formatting
st.code("print('hello')")        # Code block
```

#### **Data Display**
```python
# Dataframes
import pandas as pd
df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
st.dataframe(df)  # Interactive table
st.table(df)      # Static table

# Charts
st.line_chart(df)
st.bar_chart(df)
```

#### **Input Widgets**
```python
# Text input
name = st.text_input("Enter your name")
query = st.text_area("Enter your question", height=100)

# Buttons
if st.button("Submit"):
    st.write("Form submitted!")

# Select box
option = st.selectbox("Choose difficulty", ["easy", "medium", "hard"])

# Slider
year = st.slider("Select year", 2010, 2024, 2023)

# Multi-select
topics = st.multiselect("Select topics", ["Normalization", "SQL", "Indexing"])

# Checkbox
show_details = st.checkbox("Show details")
```

#### **Layout**
```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Sidebar
st.sidebar.title("Filters")
year = st.sidebar.slider("Year", 2010, 2024)

# Expander (collapsible section)
with st.expander("Show more details"):
    st.write("Hidden content here")

# Tabs
tab1, tab2 = st.tabs(["Search", "Analytics"])
with tab1:
    st.write("Search content")
with tab2:
    st.write("Analytics content")
```

---

### 3. API Integration

**Connecting Streamlit to FastAPI Backend:**

```python
import requests
import streamlit as st

# Configuration
API_BASE_URL = "http://localhost:8000"

def search_questions(query, year=None, difficulty=None):
    """Call backend API to search questions"""
    params = {"query": query}
    if year:
        params["year"] = year
    if difficulty:
        params["difficulty"] = difficulty

    response = requests.get(f"{API_BASE_URL}/api/search", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Error: {response.status_code}")
        return []

# Use in Streamlit app
query = st.text_input("Search questions")
if st.button("Search"):
    results = search_questions(query)
    for result in results:
        st.write(result)
```

**Error Handling:**
```python
try:
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
    response.raise_for_status()
    st.success("✅ API connected")
except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to API. Is it running?")
except requests.exceptions.Timeout:
    st.error("❌ API request timed out")
```

---

### 4. State Management

**Problem**: Streamlit reruns entire script on every interaction.

**Solution**: Session state to persist data.

```python
# Initialize state
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Add to state
query = st.text_input("Search")
if st.button("Search"):
    st.session_state.search_history.append(query)
    results = search_questions(query)
    st.session_state.last_results = results

# Display history
st.sidebar.write("Search History:")
for query in st.session_state.search_history:
    st.sidebar.write(f"- {query}")
```

**Common Use Cases:**
- Form data between pages
- User preferences
- Cache expensive computations
- Authentication state

---

### 5. Caching

**Problem**: Slow API calls or computations on every rerun.

**Solution**: Cache results.

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_courses():
    """Load courses from API (cached)"""
    response = requests.get(f"{API_BASE_URL}/api/courses")
    return response.json()

@st.cache_resource
def get_embedding_model():
    """Load ML model once (cached across all users)"""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

# Usage
courses = load_courses()  # First call: hits API
courses = load_courses()  # Second call: uses cache

model = get_embedding_model()  # Loaded once, shared
```

**Cache Types:**
- `@st.cache_data`: For data (dataframes, lists, dicts)
- `@st.cache_resource`: For resources (models, connections)

---

### 6. CourseDB-AI Frontend Architecture

**Pages:**

#### **1. Home/Search Page**
```python
# app/frontend/pages/01_🔍_Search.py
import streamlit as st
import requests

st.title("🔍 CourseDB-AI Search")

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.slider("Year", 2010, 2024, (2020, 2024))
difficulty_filter = st.sidebar.multiselect(
    "Difficulty",
    ["easy", "medium", "hard"]
)

# Search input
query = st.text_area("Enter your question or topic", height=100)

# Search type
search_type = st.radio(
    "Search method",
    ["Semantic Search", "Keyword Search", "Hybrid Search"]
)

if st.button("🔎 Search", type="primary"):
    with st.spinner("Searching..."):
        # Call API
        results = search_api(query, search_type, year_filter, difficulty_filter)

        # Display results
        st.subheader(f"Found {len(results)} questions")

        for i, result in enumerate(results, 1):
            with st.expander(f"{i}. {result['question_text'][:100]}..."):
                st.write(f"**Course:** {result['course_title']}")
                st.write(f"**Topic:** {result['topic_name']}")
                st.write(f"**Year:** {result['year']}")
                st.write(f"**Difficulty:** {result['difficulty']}")
                st.write(f"**Marks:** {result['marks']}")
                st.write(f"**Similarity:** {result['similarity']:.2%}")

                # Show similar questions
                if st.button(f"Find similar", key=f"similar_{i}"):
                    st.session_state.similarity_query = result['question_id']
```

#### **2. Analytics Dashboard**
```python
# app/frontend/pages/02_📊_Analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Analytics Dashboard")

# Load data from API
@st.cache_data(ttl=3600)
def load_analytics():
    response = requests.get(f"{API_BASE_URL}/api/analytics")
    return response.json()

data = load_analytics()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Questions", data["total_questions"])
col2.metric("Total Topics", data["total_topics"])
col3.metric("Total Courses", data["total_courses"])
col4.metric("Years Covered", data["years_covered"])

# Questions by year
st.subheader("Questions by Year")
df_year = pd.DataFrame(data["questions_by_year"])
fig = px.bar(df_year, x="year", y="count", title="Question Distribution")
st.plotly_chart(fig, use_container_width=True)

# Topic frequency
st.subheader("Most Frequent Topics")
df_topics = pd.DataFrame(data["topic_frequency"])
fig = px.pie(df_topics, values="count", names="topic_name")
st.plotly_chart(fig, use_container_width=True)

# Difficulty distribution
st.subheader("Difficulty Distribution")
df_difficulty = pd.DataFrame(data["difficulty_distribution"])
fig = px.bar(df_difficulty, x="difficulty", y="count", color="difficulty")
st.plotly_chart(fig, use_container_width=True)
```

#### **3. RAG Q&A Page**
```python
# app/frontend/pages/03_💬_Ask_AI.py
import streamlit as st

st.title("💬 Ask CourseDB-AI")

st.markdown("""
Ask questions about database concepts, and I'll answer using retrieved context
from the question database (Retrieval-Augmented Generation).
""")

question = st.text_area("Your question", height=100)

if st.button("Get Answer"):
    with st.spinner("Thinking..."):
        # Call RAG endpoint
        response = requests.post(
            f"{API_BASE_URL}/api/rag",
            json={"question": question}
        )
        result = response.json()

        # Display answer
        st.subheader("Answer:")
        st.write(result["answer"])

        # Show sources
        st.subheader("Sources:")
        for source in result["sources"]:
            with st.expander(f"📄 {source['title']}"):
                st.write(source["text"])
                st.caption(f"Year: {source['year']} | Similarity: {source['similarity']:.2%}")
```

#### **4. Admin/Upload Page**
```python
# app/frontend/pages/04_⚙️_Admin.py
import streamlit as st

st.title("⚙️ Admin Panel")

# Authentication (simple version)
password = st.text_input("Admin Password", type="password")

if password == "admin123":  # ⚠️ INSECURE DEMO ONLY — never ship hardcoded
                            # passwords. Use environment variables / a real
                            # auth provider (e.g. OAuth) in production.
    st.success("Authenticated")

    # File upload
    st.subheader("Upload Questions CSV")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:", df.head())

        if st.button("Upload to Database"):
            # Send to API
            response = requests.post(
                f"{API_BASE_URL}/api/questions/bulk",
                json=df.to_dict(orient="records")
            )
            if response.status_code == 201:
                st.success(f"Uploaded {len(df)} questions!")
            else:
                st.error("Upload failed")

    # Regenerate embeddings
    if st.button("Regenerate All Embeddings"):
        with st.spinner("Generating embeddings..."):
            response = requests.post(f"{API_BASE_URL}/api/embeddings/regenerate")
            if response.status_code == 200:
                st.success("Embeddings regenerated!")
else:
    st.warning("Please enter admin password")
```

---

### 7. Styling and UX

#### **Custom Theme**
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

#### **Custom CSS**
```python
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)
```

#### **Loading States**
```python
with st.spinner("Loading..."):
    time.sleep(2)  # Simulate work
st.success("Done!")

# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)
    time.sleep(0.01)
```

---

### 8. Deployment

#### **Option 1: Streamlit Cloud** (Free)
1. Push code to GitHub
2. Visit streamlit.io/cloud
3. Connect repository
4. Deploy!

#### **Option 2: Docker**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app/frontend/Home.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/coursedb

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://backend:8000
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=postgres
```

---

### 9. Best Practices

#### **Performance**
```python
# ✅ Good: Cache expensive operations
@st.cache_data
def load_data():
    return expensive_operation()

# ❌ Bad: No caching
def load_data():
    return expensive_operation()  # Runs on every interaction
```

#### **User Experience**
```python
# ✅ Good: Show loading states
with st.spinner("Processing..."):
    result = process_data()

# ✅ Good: Error handling with user-friendly messages
try:
    result = api_call()
except Exception as e:
    st.error("Something went wrong. Please try again.")
    st.caption(f"Error details: {str(e)}")

# ✅ Good: Input validation
query = st.text_input("Search")
if query and len(query) < 3:
    st.warning("Please enter at least 3 characters")
```

#### **Code Organization**
```python
# utils.py - Separate API calls
def api_client():
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def search_questions(self, query):
            return requests.get(f"{self.base_url}/search", params={"q": query})

    return APIClient(os.getenv("API_BASE_URL"))

# In Streamlit app
from utils import api_client
api = api_client()
results = api.search_questions(query)
```

---

## ✅ Self-Check Questions

1. What's the difference between `st.cache_data` and `st.cache_resource`?
2. How do you persist data across Streamlit reruns?
3. What's the best way to handle API errors in Streamlit?
4. How do you create multi-page Streamlit apps?
5. What's the purpose of `st.spinner`?
6. How do you deploy a Streamlit app?
7. When should you use `st.columns` vs `st.sidebar`?
8. How do you pass data between Streamlit pages?

---

## 🔬 Hands-On Exercises

### Exercise 1: Basic Streamlit App
```python
# Create app.py
import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")

age = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age} years old")

if st.button("Submit"):
    st.success("Form submitted!")
    st.balloons()  # Fun animation!
```

### Exercise 2: API Integration

> **TODO(learner):** Complete the search interface below. The `# TODO` lines
> mark *your* tasks — implement the API call and result display yourself.

```python
# Create a search interface that calls the CourseDB-AI API
import streamlit as st
import requests

def search_questions(query):
    # TODO(learner): Implement the API call (use requests.get against /search)
    pass

st.title("Question Search")
query = st.text_input("Enter search query")

if st.button("Search"):
    results = search_questions(query)
    # TODO(learner): Display the results
```

### Exercise 3: Analytics Dashboard

> **TODO(learner):** Build the dashboard below. Each `# TODO` line is a task
> for you to complete.

```python
# Create an analytics dashboard with charts
import streamlit as st
import pandas as pd
import plotly.express as px

# TODO(learner): Load data from the API
# TODO(learner): Create 3 different visualizations
# TODO(learner): Add filters (year, difficulty, topic)
```

---

## 🎓 CourseDB-AI Frontend Checklist

- [ ] Setup Streamlit project structure
- [ ] Create Home page with search
- [ ] Implement semantic search UI
- [ ] Create analytics dashboard
- [ ] Build RAG Q&A interface
- [ ] Add admin panel
- [ ] Implement caching
- [ ] Add error handling
- [ ] Style with custom CSS/theme
- [ ] Test on sample data
- [ ] Deploy to Streamlit Cloud

---

**Next Week (Week 12):** Project evaluation, portfolio building, and capstone!
