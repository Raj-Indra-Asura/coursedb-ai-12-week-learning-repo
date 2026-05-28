# Hash Index Simulator

**Week 7: Indexing, B+ Tree, Hashing**

Educational hash index for learning collision handling and trade-offs.

---

## 🎯 Key Concepts

- **Hash Function**: Maps keys to buckets (key % bucket_count)
- **Collision**: Multiple keys map to same bucket
- **Chaining**: Handle collisions with linked lists
- **Trade-off**: Fast equality, but no range queries

---

## 📊 When to Use Hash Indexes

### ✅ Good For:
- `WHERE id = 42` (exact match)
- `WHERE username = 'alice'` (equality)
- Join on exact keys

### ❌ Bad For:
- `WHERE salary > 50000` (range query)
- `WHERE age < 30` (inequality)
- `ORDER BY name` (sorting)
- `BETWEEN` queries

---

## 🧪 Running the Demo

```bash
cd dbms_internals/hash_index
python hash_index.py
```

---

## 📝 Exercises

1. Insert keys [12, 22, 32] into 10-bucket hash. Where do they go?
2. Why do these keys collide?
3. What happens if we use 100 buckets instead of 10?

---

## 🔍 Self-Check

1. What is a hash collision?
2. How does chaining handle collisions?
3. Why can't hash indexes do range queries?
4. When would you choose hash over B+ tree?

**Answers in Week 7 reflection.md**
