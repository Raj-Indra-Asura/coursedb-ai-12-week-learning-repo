# Week 11: Frontend Integration - Common Mistakes

## 🎯 Avoiding Pitfalls

---

## Mistake 1: Not Caching API Calls

**What happens:**
```python
def load_data():
    response = requests.get("http://localhost:8000/api/courses")
    return response.json()

# Called on EVERY user interaction!
courses = load_data()  # Slow!
```

**Fix:**
```python
@st.cache_data(ttl=3600)
def load_data():
    response = requests.get("http://localhost:8000/api/courses")
    return response.json()

courses = load_data()  # Fast!
```

---

## Mistake 2: Not Initializing State

**What happens:**
```python
# KeyError if not initialized!
results = st.session_state.results
```

**Fix:**
```python
if 'results' not in st.session_state:
    st.session_state.results = []

results = st.session_state.results  # Safe
```

---

## Mistake 3: Ignoring Errors

**What happens:**
```python
response = requests.get(url)
data = response.json()  # Crashes if API down!
```

**Fix:**
```python
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"API Error: {e}")
    data = None
```

---

## Mistake 4: No Loading Indicators

**What happens:**
```python
# User sees nothing while API loads
results = slow_api_call()
```

**Fix:**
```python
with st.spinner("Loading..."):
    results = slow_api_call()

st.success("Loaded!")
```

---

## Mistake 5: Inefficient Reruns

**What happens:**
```python
# Every interaction triggers recomputation
expensive_data = compute_something_slow()
```

**Fix:**
```python
@st.cache_data
def compute_something_slow():
    # Only computed once
    return expensive_result
```

---

## Mistake 6: Poor UX

**What happens:**
- No placeholders in inputs
- No feedback messages
- Unclear error messages
- No help text

**Fix:**
```python
query = st.text_input(
    "Search query",
    placeholder="Enter question...",
    help="Use keywords or natural language"
)

if st.button("Search"):
    if not query:
        st.warning("Please enter a query")
    else:
        st.success("Search complete!")
```

---

## Mistake 7: Not Using Forms

**What happens:**
```python
# App reruns on EVERY input change!
name = st.text_input("Name")
email = st.text_input("Email")
age = st.slider("Age", 0, 100)
```

**Fix:**
```python
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.slider("Age", 0, 100)
    
    # Only reruns on submit
    submit = st.form_submit_button("Submit")
```

---

## Mistake 8: Hardcoded API URLs

**What happens:**
```python
API_URL = "http://localhost:8000"  # Breaks in production!
```

**Fix:**
```python
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Or use Streamlit secrets
API_URL = st.secrets.get("API_URL", "http://localhost:8000")
```

---

## Mistake 9: No Mobile Consideration

**What happens:**
- Wide layouts don't work on mobile
- Too many columns
- Small text

**Fix:**
```python
# Use responsive columns
cols = st.columns([1, 2, 1])  # Ratios work better

# Limit column count
if st.session_state.get('mobile', False):
    cols = st.columns(1)
else:
    cols = st.columns(3)
```

---

## Mistake 10: Overusing st.rerun()

**What happens:**
```python
if st.button("Click"):
    st.session_state.counter += 1
    st.rerun()  # Usually unnecessary!
```

**Fix:**
```python
# Streamlit auto-reruns on interactions
if st.button("Click"):
    st.session_state.counter += 1
    # No st.rerun() needed
```

---

## Best Practices Summary

1. **Always cache** API calls and expensive operations
2. **Initialize state** before accessing
3. **Handle errors** gracefully with try/except
4. **Show feedback** with spinners and messages
5. **Use forms** for multiple related inputs
6. **Provide UX hints** with placeholders and help text
7. **Test thoroughly** with different inputs
8. **Use environment variables** for configuration

---

**Remember:** Good error handling and UX make the difference between a demo and production app!
