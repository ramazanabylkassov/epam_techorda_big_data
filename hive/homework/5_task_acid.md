# Hive ACID Tables

This guide covers the fifth homework task exploring ACID (Atomicity, Consistency, Isolation, Durability) transactional tables in Hive, enabling UPDATE, DELETE, and MERGE operations.

## Learning Objectives

- Understand ACID requirements in Hive
- Create transactional tables with ORC format and bucketing
- Perform DML operations (INSERT, UPDATE, DELETE)
- Verify transactional properties using DESCRIBE FORMATTED

---

## Prerequisites: Enable ACID Settings

Before creating or working with ACID tables, run these required settings in your Hive session:

```sql
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
```

> **Important:** These settings only apply to the current session. Run them each time you reconnect to Beeline or Hue.

### What Each Setting Does

| Setting | Purpose |
|---------|---------|
| `hive.txn.manager=...DbTxnManager` | Enables the transaction manager that supports UPDATE, DELETE, and MERGE operations. Without this, Hive operates in append-only mode. |
| `hive.support.concurrency=true` | Enables concurrency control and locking, allowing multiple users to safely read/write ACID tables simultaneously. |
| `hive.enforce.bucketing=true` | Enforces bucketing rules required for ACID tables. Ensures INSERT/UPDATE/DELETE operations are applied consistently across buckets. |
| `hive.exec.dynamic.partition.mode=nonstrict` | Allows dynamic partition creation without requiring static partition values. |

---

## Task Walkthrough

### Step 1: Create a Transactional ACID Table

ACID tables in Hive require:

- **ORC file format** (supports row-level metadata)
- **Bucketing** (ensures deterministic file placement)
- **Transactional property** set to true

```sql
CREATE TABLE my_emp (
  id INT,
  name STRING,
  salary INT
)
CLUSTERED BY (id) INTO 2 BUCKETS
STORED AS ORC
TBLPROPERTIES ('transactional'='true');
```

---

### Step 2: Verify Table Supports DML Operations

```sql
DESCRIBE FORMATTED my_emp;
```

Look for the `transactional` property in the output:

```
transactional           true
```

This confirms the table supports:

- INSERT
- UPDATE
- DELETE
- MERGE

#### Homework Question and Answer

**Q: Which DESCRIBE operation is required to check if a table supports DML operations?**

**A:** `DESCRIBE FORMATTED my_emp` — This shows all table properties including the `transactional` flag that indicates ACID support.

---

### Step 3: Insert 3 Rows in a Single Command

```sql
INSERT INTO my_emp VALUES
  (1, 'John', 10000),
  (2, 'Sara', 12000),
  (3, 'Adam', 8000);
```

---

### Step 4: Verify Rows Were Inserted

```sql
SELECT * FROM my_emp;
```

Expected output:

| id | name | salary |
|----|------|--------|
| 1 | John | 10000 |
| 2 | Sara | 12000 |
| 3 | Adam | 8000 |

---

### Step 5: Update Adam's Salary

```sql
UPDATE my_emp
SET salary = 9000
WHERE name = 'Adam';
```

---

### Step 6: Insert a New Row (Alex)

```sql
INSERT INTO my_emp VALUES (4, 'Alex', 13000);
```

---

### Step 7: Delete John from the Table

```sql
DELETE FROM my_emp
WHERE name = 'John';
```

---

### Step 8: Verify All Changes

```sql
SELECT * FROM my_emp;
```

Expected final output:

| id | name | salary |
|----|------|--------|
| 2 | Sara | 12000 |
| 3 | Adam | 9000 |
| 4 | Alex | 13000 |

Verification checklist:

- ✅ John is deleted
- ✅ Adam's salary updated from 8000 to 9000
- ✅ Alex is inserted

---

## Key Concepts

### What is ACID?

ACID is a set of properties that guarantee reliable database transactions:

| Property | Description |
|----------|-------------|
| **Atomicity** | Operations happen fully or not at all. A transaction either completes entirely or rolls back. |
| **Consistency** | The database remains in a valid state before and after transactions. |
| **Isolation** | Concurrent transactions don't interfere with each other. |
| **Durability** | Once committed, changes persist even after system failures. |

### What Does "Transactional" Mean in Hive?

When a table has `'transactional'='true'`:

- The table becomes an **ACID table**
- It supports row-level modifications (UPDATE, DELETE)
- Hive manages delta files, base files, and compaction automatically

| Operation | Non-Transactional Table | Transactional Table |
|-----------|------------------------|---------------------|
| INSERT | ✅ | ✅ |
| UPDATE | ❌ | ✅ |
| DELETE | ❌ | ✅ |
| MERGE | ❌ | ✅ |

### Why ORC + Bucketing Are Required

Hive implements ACID by maintaining:

- **Base files** — Original data snapshots
- **Delta files** — Records of changes (inserts, updates, deletes)
- **Compaction jobs** — Periodic merging of deltas into base files

These mechanisms require:

| Requirement | Reason |
|-------------|--------|
| **ORC format** | Supports row-level metadata, efficient columnar storage, and delta tracking |
| **Bucketing** | Ensures deterministic file placement so UPDATE/DELETE can locate specific rows |

---

## Summary: ACID Table Requirements

```sql
CREATE TABLE table_name (
  columns...
)
CLUSTERED BY (column) INTO n BUCKETS    -- Required: bucketing
STORED AS ORC                            -- Required: ORC format
TBLPROPERTIES ('transactional'='true'); -- Required: transactional flag
```

Plus session settings:

```sql
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
```

---

## Quick Reference: Complete Command Sequence

```sql
-- Enable ACID settings (run first!)
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

-- Create transactional table
CREATE TABLE my_emp (
  id INT,
  name STRING,
  salary INT
)
CLUSTERED BY (id) INTO 2 BUCKETS
STORED AS ORC
TBLPROPERTIES ('transactional'='true');

-- Verify transactional property
DESCRIBE FORMATTED my_emp;

-- Insert initial data
INSERT INTO my_emp VALUES
  (1, 'John', 10000),
  (2, 'Sara', 12000),
  (3, 'Adam', 8000);

-- Verify insert
SELECT * FROM my_emp;

-- Update Adam's salary
UPDATE my_emp SET salary = 9000 WHERE name = 'Adam';

-- Insert new employee
INSERT INTO my_emp VALUES (4, 'Alex', 13000);

-- Delete John
DELETE FROM my_emp WHERE name = 'John';

-- Verify all changes
SELECT * FROM my_emp;
```

---

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Attempt to do update or delete using transaction manager that does not support these operations` | Transaction manager not set | Run `SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;` |
| `Cannot perform UPDATE/DELETE on table without ACID support` | Table not transactional | Recreate table with `TBLPROPERTIES ('transactional'='true')` |
| `Table must be bucketed for transactional` | Missing CLUSTERED BY clause | Add `CLUSTERED BY (column) INTO n BUCKETS` to CREATE TABLE |
| `ORC format required for ACID` | Wrong file format | Use `STORED AS ORC` |