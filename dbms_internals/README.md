# DBMS Internals: Educational Simulators

This directory contains educational implementations of DBMS internal concepts.

**Important**: These are for learning, not production use.

---

## 📁 Modules

### 1. B+ Tree Visualizer (`bplus_tree/`)

**Purpose**: Understand B+ tree insertion, search, and node splits

**What it teaches**:
- B+ tree structure (internal nodes, leaf nodes)
- Key insertion algorithm
- Node splitting when capacity exceeded
- Search path visualization

**When to study**: Week 7 (Indexing, B+ Tree, Hashing)

**Usage**:
```python
from dbms_internals.bplus_tree.bplus_tree import BPlusTree

tree = BPlusTree(order=3)
tree.insert(10)
tree.insert(20)
tree.insert(5)
tree.visualize()
```

---

### 2. Hash Index Simulator (`hash_index/`)

**Purpose**: Understand hash-based indexing and collision handling

**What it teaches**:
- Hash function (key % bucket_count)
- Collision handling (chaining)
- Equality lookups (fast)
- Range queries (impossible)
- Comparison with B+ trees

**When to study**: Week 7 (Indexing, B+ Tree, Hashing)

**Usage**:
```python
from dbms_internals.hash_index.hash_index import HashIndex

index = HashIndex(num_buckets=10)
index.insert(key=42, value="Question about normalization")
result = index.search(42)
```

---

### 3. Query Plan Analyzer (`query_plan/`)

**Purpose**: Understand PostgreSQL EXPLAIN and query optimization

**What it teaches**:
- Sequential scan vs index scan
- Cost estimation
- Actual execution time
- Impact of indexes on performance

**When to study**: Week 8 (Query Optimization + EXPLAIN)

**Contents**:
- `query_plan_demo.sql`: SQL queries with EXPLAIN ANALYZE
- `outputs/before_indexes.txt`: Results before indexing
- `outputs/after_indexes.txt`: Results after indexing
- `README.md`: Analysis and interpretation

---

### 4. Transaction & Concurrency (`transactions/`)

**Purpose**: Understand transactions, ACID, concurrency, deadlocks

**What it teaches**:
- COMMIT and ROLLBACK
- Transaction isolation
- Concurrent transaction issues
- Deadlock detection with wait-for graph

**When to study**: Week 9 (Transactions, ACID, Concurrency)

**Contents**:
- `transaction_demo.sql`: PostgreSQL transaction examples
- `wait_for_graph.py`: Deadlock detection visualization
- `tests/`: Transaction behavior tests

**Usage**:
```python
from dbms_internals.transactions.wait_for_graph import WaitForGraph

wfg = WaitForGraph()
wfg.add_edge("T1", "T2")  # T1 waits for T2
wfg.add_edge("T2", "T3")
wfg.add_edge("T3", "T1")  # Creates cycle
cycles = wfg.detect_deadlock()
wfg.visualize()
```

---

## 🎓 Learning Approach

### Before Using These Modules

1. **Study theory first**: Read textbook chapters, watch lectures
2. **Work through examples by hand**: Draw B+ trees on paper
3. **Predict behavior**: Before running code, predict what will happen
4. **Run and verify**: Check if your prediction was correct

### While Using These Modules

1. **Read the code**: Don't just run it
2. **Add print statements**: Trace execution flow
3. **Modify and experiment**: Change parameters, break things
4. **Document observations**: Note surprising behaviors

### After Using These Modules

1. **Write your own version**: Implement a simpler version from scratch
2. **Explain to someone**: Teach the concept to a peer or AI
3. **Connect to CourseDB-AI**: How does PostgreSQL use these internally?
4. **Reflect**: Update your learning log

---

## ⚠️ Limitations

These are **educational simulators**, not production implementations:

❌ B+ tree: No deletion, no rebalancing, simplified node structure
❌ Hash index: Basic chaining, no extendible/linear hashing
❌ Query plans: PostgreSQL-specific, simplified interpretation
❌ Transactions: Demonstrations, not actual concurrency control

✅ Use these to **understand concepts**
✅ Use PostgreSQL for **real applications**

---

## 🧪 Testing

Each module has tests:

```bash
# Test B+ tree
pytest dbms_internals/bplus_tree/tests/

# Test hash index
pytest dbms_internals/hash_index/tests/

# Test transactions
pytest dbms_internals/transactions/tests/
```

---

## 📚 Documentation

Each module has its own README:
- `bplus_tree/README.md`
- `hash_index/README.md`
- `query_plan/README.md`
- `transactions/README.md`

---

## 🔗 Related Docs

- `docs/indexing/`: Indexing theory and practice
- `docs/transactions/`: Transaction theory
- `docs/architecture/`: How these fit into CourseDB-AI

---

**Remember**: The goal is understanding, not perfect code. Break things, experiment, learn!
