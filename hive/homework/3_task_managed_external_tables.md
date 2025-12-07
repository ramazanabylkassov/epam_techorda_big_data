# Managed and External Tables Using Beeline

This guide covers the third homework task exploring the differences between Managed and External tables in Hive, including their behavior during DROP operations and how data is stored in HDFS.

## Learning Objectives

- Understand the difference between MANAGED and EXTERNAL tables
- Inspect table properties using `DESCRIBE FORMATTED`
- Observe how DROP TABLE behaves differently for each table type
- Navigate and manipulate HDFS directories via CLI

---

## Task Walkthrough

### Step 1: Connect to Hive Using Beeline

Open a bash session to the Docker container and connect:

```bash
docker exec -it docker-hive-hive-server-1 /bin/bash
beeline -u jdbc:hive2://localhost:10000 -n hive
```

---

### Step 2: Verify newdb.new_emp is Populated

```sql
USE newdb;
SELECT COUNT(*) FROM new_emp;
```

Expected output: Row count matching the original `classicmodels.employees` table (e.g., 23 rows).

---

### Step 3: Inspect Table Properties

Run the verbose describe command to view all table properties:

```sql
DESCRIBE FORMATTED new_emp;
```

#### Key Properties to Identify:

| Property | Where to Find | Example Value |
|----------|---------------|---------------|
| **HDFS Location** | `Location:` field | `hdfs://namenode:8020/user/hive/warehouse/newdb.db/new_emp` |
| **File Type** | `InputFormat:` field | `org.apache.hadoop.mapred.TextInputFormat` (indicates TEXTFILE) |
| **Table Type** | `Table Type:` field | `MANAGED_TABLE` |
| **Number of Files (Table Parameters)** | `numFiles:` field | `1` | 

> **Note:** Tables created with CTAS (`CREATE TABLE AS SELECT`) are MANAGED by default.

---

### Step 4: Examine HDFS Directory via CLI

Exit Beeline:

```sql
!quit
```

From the container terminal, inspect the HDFS directory:

#### List Files

```bash
hdfs dfs -ls /user/hive/warehouse/newdb.db/new_emp
```

Expected output:

```
Found 1 items
-rw-r--r--   1 hive supergroup    ... /user/hive/warehouse/newdb.db/new_emp/000000_0
```

#### Count Files

```bash
hdfs dfs -count /user/hive/warehouse/newdb.db/new_emp
```

#### View File Contents

```bash
hdfs dfs -cat /user/hive/warehouse/newdb.db/new_emp/000000_0 | head
```

#### Is the File Human-Readable?

**Yes** — The file is human-readable because:

- The table uses **TEXTFILE** format (default for CTAS)
- Data is stored as plain text with fields separated by the default Hive delimiter (`\001` / Ctrl-A)
- The `InputFormat` property (`TextInputFormat`) confirms this is a text-based storage format

---

### Step 5: Drop the MANAGED Table

Reconnect to Beeline:

```bash
beeline -u jdbc:hive2://localhost:10000 -n hive
```

Drop the table:

```sql
USE newdb;
DROP TABLE new_emp;
```

Exit and check HDFS:

```bash
hdfs dfs -ls /user/hive/warehouse/newdb.db/new_emp
```

Expected output:

```
ls: `/user/hive/warehouse/newdb.db/new_emp': No such file or directory
```

#### Explanation

**MANAGED TABLE behavior:** When a managed table is dropped, Hive deletes **both** the metadata (table definition) **and** the underlying data files in HDFS. This is because Hive "owns" the data for managed tables.

---

### Step 6: Attempt to Create EXTERNAL Table with CTAS

Reconnect to Beeline and try:

```sql
USE newdb;
CREATE EXTERNAL TABLE new_emp AS
SELECT * FROM classicmodels.employees;
```

#### Expected Error

```
FAILED: SemanticException [Error 10070]: CREATE-TABLE-AS-SELECT cannot create external table
```

#### Explanation

Hive does not allow combining `CREATE EXTERNAL TABLE` with `AS SELECT` (CTAS) in a single statement. This is by design because:

- External tables expect data to already exist at a specified location
- CTAS generates new data, which contradicts the external table concept
- The workaround is to create a managed table first, then convert it to external

---

### Step 7: Create MANAGED Table and Convert to EXTERNAL

#### Step 7.1: Create as MANAGED (Default)

```sql
CREATE TABLE new_emp AS
SELECT * FROM classicmodels.employees;
```

#### Step 7.2: Convert to EXTERNAL

```sql
ALTER TABLE new_emp SET TBLPROPERTIES ('EXTERNAL'='TRUE');
```

#### Step 7.3: Verify the Change

```sql
DESCRIBE FORMATTED new_emp;
```

Confirm `Table Type:` now shows:

```
Table Type:         EXTERNAL_TABLE
```

---

### Step 8: Re-check Table Properties

```sql
DESCRIBE FORMATTED new_emp;
```

Record the following:

| Property | Value |
|----------|-------|
| Location | `hdfs://namenode:8020/user/hive/warehouse/newdb.db/new_emp` |
| InputFormat | `org.apache.hadoop.mapred.TextInputFormat` (TEXTFILE) |
| Table Type | `EXTERNAL_TABLE` |

> **Note:** The location and file format remain unchanged after converting to external — only the table type property changes.

---

### Step 9: Examine HDFS Directory Again

Exit Beeline and check:

```bash
hdfs dfs -ls /user/hive/warehouse/newdb.db/new_emp
```

Files should still exist:

```bash
hdfs dfs -count /user/hive/warehouse/newdb.db/new_emp
```

---

### Step 10: Drop the EXTERNAL Table

Reconnect to Beeline:

```bash
beeline -u jdbc:hive2://localhost:10000 -n hive
```

Drop the table:

```sql
USE newdb;
DROP TABLE new_emp;
```

Exit and check HDFS:

```bash
hdfs dfs -ls /user/hive/warehouse/newdb.db/new_emp
```

Expected output: **Files still exist!**

```
Found 1 items
-rw-r--r--   1 hive supergroup    ... /user/hive/warehouse/newdb.db/new_emp/000000_0
```

#### Explanation

**EXTERNAL TABLE behavior:** When an external table is dropped, Hive deletes **only** the metadata (table definition). The underlying data files in HDFS are **preserved**. This is because Hive does not "own" the data for external tables — it only references it.

---

### Step 11: Manually Remove the HDFS Folder

Since the data persists after dropping an external table, remove it manually:

```bash
hdfs dfs -rm -r /user/hive/warehouse/newdb.db/new_emp
```

Verify removal:

```bash
hdfs dfs -ls /user/hive/warehouse/newdb.db
```

The `new_emp` directory should no longer appear.

---

## Summary: Managed vs External Tables

| Behavior | MANAGED Table | EXTERNAL Table |
|----------|---------------|----------------|
| **Data ownership** | Hive owns the data | Hive references the data |
| **Default location** | `/user/hive/warehouse/<db>.db/<table>` | User-specified or default |
| **DROP TABLE** | Deletes metadata AND data | Deletes metadata ONLY |
| **Use case** | Temporary/intermediate data | Shared data, data managed outside Hive |
| **CTAS support** | ✅ Yes | ❌ No (must create then alter) |

---

## Key Commands Reference

| Task | Command |
|------|---------|
| View all table properties | `DESCRIBE FORMATTED <table>;` |
| Convert managed to external | `ALTER TABLE <table> SET TBLPROPERTIES ('EXTERNAL'='TRUE');` |
| Convert external to managed | `ALTER TABLE <table> SET TBLPROPERTIES ('EXTERNAL'='FALSE');` |
| List HDFS directory | `hdfs dfs -ls <path>` |
| View HDFS file contents | `hdfs dfs -cat <path>` |
| Count files in HDFS | `hdfs dfs -count <path>` |
| Remove HDFS directory | `hdfs dfs -rm -r <path>` |

---

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `CREATE-TABLE-AS-SELECT cannot create external table` | CTAS not supported with EXTERNAL | Create as managed, then `ALTER TABLE ... SET TBLPROPERTIES ('EXTERNAL'='TRUE')` |
| `No such file or directory` after DROP | Expected for MANAGED tables | Data was deleted as designed |
| Files persist after DROP | Expected for EXTERNAL tables | Manually remove with `hdfs dfs -rm -r` |