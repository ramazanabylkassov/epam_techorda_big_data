# Basic Hive Interaction Using Beeline

This guide covers the second homework task demonstrating Hive operations via the Beeline command-line interface.

## Overview

Beeline is a JDBC client for HiveServer2. Unlike the older Hive CLI, Beeline connects to Hive through a JDBC connection, making it the recommended method for interacting with Hive from the command line.

---

## Task Walkthrough

### Step 1: Connect to Hive Using Beeline

Open a bash session to the Docker container and connect to Hive:

```bash
beeline -u jdbc:hive2://localhost:10000 -n hive
```

| Parameter | Description |
|-----------|-------------|
| `-u` | JDBC connection URL to HiveServer2 |
| `jdbc:hive2://localhost:10000` | Default HiveServer2 endpoint |
| `-n hive` | Username for connection |

Upon successful connection, you'll see the Beeline prompt:

```
0: jdbc:hive2://localhost:10000>
```

---

### Step 2: Show Available Databases

Verify that the `classicmodels` database exists:

```sql
SHOW DATABASES;
```

Expected output should include:

```
+----------------+
| database_name  |
+----------------+
| classicmodels  |
| default        |
+----------------+
```

---

### Step 3: Switch to the ClassicModels Database

```sql
USE classicmodels;
```

> **Note:** Unlike Hue, the `USE` command persists within a Beeline session, so subsequent queries don't require explicit database prefixes.

---

### Step 4: Show All Tables in the Database

```sql
SHOW TABLES;
```

Expected output:

```
+--------------+
|   tab_name   |
+--------------+
| customers    |
| employees    |
| offices      |
| orderdetails |
| payments     |
| products     |
+--------------+
```

---

### Step 5: Create a New Database

Create the `newdb` database:

```sql
CREATE DATABASE newdb;
```

Verify the database was created:

```sql
SHOW DATABASES;
```

Expected output should now include `newdb`:

```
+----------------+
| database_name  |
+----------------+
| classicmodels  |
| default        |
| newdb          |
+----------------+
```

---

### Step 6: Create Table Identical to Employees

Switch to the new database:

```sql
USE newdb;
```

Create `new_emp` table with schema and data from `classicmodels.employees` using CTAS (Create Table As Select):

```sql
CREATE TABLE new_emp AS
SELECT * FROM classicmodels.employees;
```

This single command:
- Creates a new table with the same column structure as the source
- Copies all data from `classicmodels.employees` into `new_emp`

---

### Step 7: Verify the Table is Populated

```sql
SELECT COUNT(*) FROM new_emp;
```

The count should match the number of rows in the original employees table.

Optional — verify schema matches:

```sql
DESCRIBE new_emp;
```

---

## Quick Reference: Complete Command Sequence

```sql
-- Connect to Hive
-- beeline -u jdbc:hive2://localhost:10000 -n hive

-- Verify classicmodels exists
SHOW DATABASES;

-- Switch to classicmodels
USE classicmodels;

-- Show tables
SHOW TABLES;

-- Create new database
CREATE DATABASE newdb;
SHOW DATABASES;

-- Create identical table in newdb
USE newdb;
CREATE TABLE new_emp AS
SELECT * FROM classicmodels.employees;

-- Verify data
SELECT COUNT(*) FROM new_emp;
```

---

## Key Concepts

### Beeline vs Hive CLI

| Feature | Beeline | Hive CLI (Deprecated) |
|---------|---------|----------------------|
| Connection | JDBC to HiveServer2 | Direct to Hive |
| Security | Supports authentication | Limited |
| Concurrency | Multi-user support | Single-user |
| Status | Recommended | Deprecated |

### CTAS (Create Table As Select)

The `CREATE TABLE ... AS SELECT` statement is a convenient way to:
- Create a new table based on the results of a query
- Copy both schema and data in a single operation
- The new table inherits data types from the query results

```sql
CREATE TABLE new_table AS
SELECT * FROM existing_table;
```

---

## Exiting Beeline

To exit the Beeline session:

```sql
!quit
```

Or use `Ctrl+D`.