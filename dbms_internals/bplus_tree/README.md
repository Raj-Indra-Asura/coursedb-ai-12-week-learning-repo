# B+ Tree Visualizer

**Week 7: Indexing, B+ Tree, Hashing**

---

## 🎯 Learning Objectives

- Understand B+ tree structure and properties
- Visualize node splits during insertion
- Compare B+ trees with binary search trees
- Understand why databases use B+ trees

---

## 📚 Theory: What is a B+ Tree?

A **B+ tree** is a self-balancing tree optimized for systems that read and write large blocks of data (like databases).

### Key Properties

1. **All data in leaves**: Internal nodes only store keys for navigation
2. **Linked leaves**: Leaves form a linked list (efficient range scans)
3. **Balanced**: All leaves at same depth
4. **High fanout**: Each node has many children (reduces height)

### Why B+ Trees for Databases?

| Feature | Benefit |
|---------|---------|
| **High fanout** | Fewer disk I/O operations |
| **All data at leaves** | Consistent access time |
| **Linked leaves** | Efficient range queries |
| **Self-balancing** | Predictable performance |

---

## 🔧 Implementation

### Order

**Order (m)**: Maximum number of children per node

- Educational example: `m=3` (easier to visualize)
- Real database: `m=100-200` (fits one disk page)

### Node Structure

```python
class BPlusTreeNode:
    order: int           # Maximum children
    keys: List[int]      # Keys for navigation/data
    children: List       # Child nodes or data
    is_leaf: bool        # True for leaf nodes
    next: Node           # Next leaf (for range scans)
```

---

## 🎨 Visualization Example

### Insertion Sequence: 10, 20, 5, 6, 12, 30, 7

**Order = 3** (each node can have 2-3 children)

#### Step 1: Insert 10, 20, 5
```
[5, 10, 20]  (all fit in root leaf)
```

#### Step 2: Insert 6 (causes split)
```
       [10]            (new root, internal node)
      /    \
  [5, 6]  [10, 20]     (two leaf nodes, linked)
```

#### Step 3: Insert 12
```
       [10]
      /    \
  [5, 6]  [10, 12, 20]
```

#### Step 4: Insert 30 (causes split)
```
          [10, 20]      (root splits)
         /   |    \
    [5,6] [10,12] [20,30]
```

#### Step 5: Insert 7
```
          [10, 20]
         /   |    \
  [5,6,7] [10,12] [20,30]
```

---

## 📝 Exercises

### Exercise 1: Manual Insertion

Given a B+ tree with order=3, manually insert:
- 15, 25, 35, 45, 50

Draw the tree after each insertion. Identify when splits occur.

### Exercise 2: Search Path

In the final tree from the demo, trace the search path for:
- Key 12
- Key 8 (not found)

### Exercise 3: Range Query

In the final tree, list all keys in range [6, 20]. Explain how linked leaves help.

---

## 🧪 Running the Demo

```bash
cd dbms_internals/bplus_tree
python bplus_tree.py
```

Expected output:
```
=== B+ Tree Demo ===
Order: 3 (max 3 children per node)

Inserting 10...
Level 0 (leaf): [10]

Inserting 20...
Level 0 (leaf): [10, 20]

...
```

---

## 🐛 Debugging Exercise

**Note**: The B+ tree implementation in `bplus_tree.py` is **complete and
tested** — it is a working reference, not a set of stubs.

To get hands-on practice, try this exercise:
1. Read the demo sequence and predict the tree shape after each insert
2. Re-implement the `insert` method yourself in a scratch file, then compare
   with the reference
3. Add an extra test case and verify it passes
4. Document anything that surprised you in `weeks/week_07_*/reflection.md`

---

## 🔍 Self-Check Questions

1. What is the difference between a B+ tree and a B tree?
2. Why do databases prefer B+ trees over binary search trees?
3. What is the maximum height of a B+ tree with 1 million keys and order 100?
4. Why are leaves linked in a B+ tree?
5. What happens when a node overflows?
6. How does B+ tree support efficient range queries?

**Answers**:
1. B+ tree stores all data in leaves; B tree stores data in all nodes
2. Higher fanout → fewer disk I/O, better cache locality
3. log₁₀₀(1,000,000) ≈ 3 levels (amazing!)
4. For efficient sequential and range scans
5. Node splits, middle key promoted to parent
6. Find start, scan leaves left-to-right using links

---

## 📊 Comparison: B+ Tree vs Binary Search Tree

| Metric | Binary Search Tree | B+ Tree (order=100) |
|--------|-------------------|---------------------|
| **Height** (1M keys) | ~20 | ~3 |
| **Disk I/O** (search) | ~20 reads | ~3 reads |
| **Range query** | O(n) | O(log n + k) |
| **Sorted scan** | O(n) tree traversal | O(k) leaf scan |

---

## 🚀 Next Steps

- **Week 8**: Use this knowledge to understand PostgreSQL EXPLAIN output
- **Real indexes**: PostgreSQL B-tree (similar to B+ tree)
- **Advanced**: Concurrency control in B+ trees (locking, latches)

---

## 📚 Further Reading

- Database System Concepts (Silberschatz) - Chapter 11
- PostgreSQL B-tree Index: https://www.postgresql.org/docs/current/btree.html
- Visualization tool: https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html

---

**Remember**: This is an educational implementation. Real database B+ trees handle concurrency, persistence, and many optimizations not covered here.
