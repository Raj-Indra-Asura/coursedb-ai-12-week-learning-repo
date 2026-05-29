# Transaction & Concurrency Demos

**Week 9: Transactions, ACID, Concurrency**

Learn transaction safety and deadlock detection.

---

## 🎯 Key Concepts

- **ACID**: Atomicity, Consistency, Isolation, Durability
- **Transaction**: Unit of work (all or nothing)
- **Deadlock**: Cycle of transactions waiting for each other
- **Wait-For Graph**: Tool to detect deadlocks

---

## 🔄 Running Demos

### Transaction SQL Demo
```bash
psql -U postgres -d coursedb
\i dbms_internals/transactions/transaction_demo.sql
```

### Wait-For Graph
```bash
python dbms_internals/transactions/wait_for_graph.py
```

---

## 📝 Exercises

1. Run COMMIT demo. Check audit_logs.
2. Run ROLLBACK demo. Verify data unchanged.
3. Simulate deadlock with two psql sessions.
4. Use wait_for_graph.py to detect cycle.

---

## 🔍 Self-Check

1. What is a transaction?
2. What happens on ROLLBACK?
3. How does PostgreSQL detect deadlocks?
4. What is a wait-for graph cycle?

**Document in Week 9 reflection.md**
