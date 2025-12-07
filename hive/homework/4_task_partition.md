# Partitioned Tables in Hive

This guide covers the fourth homework task exploring table partitioning in Hive, including creating partitioned tables, dynamic partition insertion, and understanding partition pruning for query optimization.

## Learning Objectives

- Create partitioned tables with AVRO file format
- Insert data with dynamic partitioning
- Understand partition pruning and its impact on query performance
- Examine HDFS directory structure for partitioned tables

---

## Task Walkthrough

### Step 1: Preview Customer Data

```sql
USE classicmodels;
SELECT * FROM customers LIMIT 20;
```

This confirms the table is accessible and shows sample data structure.

---

### Step 2: Count Customers by Country

```sql
SELECT country, COUNT(*) AS cnt
FROM customers
GROUP BY country
ORDER BY cnt DESC;
```

This query shows the distribution of customers across countries, which helps understand how partitions will be distributed.

---

### Step 3: Get the DDL of the Customers Table

```sql
SHOW CREATE TABLE customers;
```

Output (example):

```sql
CREATE EXTERNAL TABLE `customers`(
  `customernumber` int,
  `customername` string,
  `contactlastname` string,
  `contactfirstname` string,
  `phone` string,
  `addressline1` string,
  `addressline2` string,
  `city` string,
  `state` string,
  `postalcode` string,
  `country` string,
  `salesrepemployeenumber` int,
  `creditlimit` double)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/classicmodels.db/customers'
```

---

### Step 4: Create the Partitioned Table

Copy the column definitions and modify to create a new partitioned table with the following requirements:

- **Database:** classicmodels
- **Table name:** cust_country
- **Partitioned by:** country column
- **File type:** AVRO

```sql
USE classicmodels;

CREATE TABLE cust_country (
  customernumber INT,
  customername STRING,
  contactlastname STRING,
  contactfirstname STRING,
  phone STRING,
  addressline1 STRING,
  addressline2 STRING,
  city STRING,
  state STRING,
  postalcode STRING,
  salesrepemployeenumber INT,
  creditlimit DOUBLE
)
PARTITIONED BY (country STRING)
STORED AS AVRO;
```

> **Note:** The `country` column is removed from the column list and specified in `PARTITIONED BY` instead. AVRO format does not require `ROW FORMAT` specification.

---

### Step 5: Verify Table Creation

```sql
DESCRIBE FORMATTED cust_country;
```

Verify the following properties:

| Property | Expected Value |
|----------|----------------|
| Table Type | `MANAGED_TABLE` |
| InputFormat | `org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat` |
| OutputFormat | `org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat` |
| Partition Columns | `country` (string) |
| Location | `/user/hive/warehouse/classicmodels.db/cust_country` |

---

### Step 6: Insert Data with Dynamic Partitioning

#### Enable Dynamic Partitioning

Before inserting data, enable dynamic partition mode:

```sql
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
```

> **Important:** These settings only apply to the current session. If you reconnect to Beeline, you must run them again.

#### Why These Settings Are Required

| Setting | Default | Purpose |
|---------|---------|---------|
| `hive.exec.dynamic.partition` | `false` | Enables dynamic partition creation |
| `hive.exec.dynamic.partition.mode` | `strict` | `strict` requires at least one static partition; `nonstrict` allows fully dynamic partitioning |

#### Insert Data

```sql
INSERT INTO TABLE cust_country
PARTITION (country)
SELECT 
  customernumber,
  customername,
  contactlastname,
  contactfirstname,
  phone,
  addressline1,
  addressline2,
  city,
  state,
  postalcode,
  salesrepemployeenumber,
  creditlimit,
  country
FROM customers
LIMIT 50;
```

> **Critical Rule:** The partition column (`country`) must be the **last column** in the SELECT clause.

> **Note:** If you receive `MoveTask` errors, you can ignore them as stated in the assignment. The data will still be inserted correctly.

#### Verify Partitions Were Created

```sql
SHOW PARTITIONS cust_country;
```

Expected output:

```
country=Australia
country=France
country=Spain
country=USA
...
```

---

### Step 7: Query USA Customers

```sql
SELECT * FROM cust_country WHERE country = 'USA';
```

This query returns only customers from the USA partition.

---

### Step 8: Examine the Execution Plan

#### Basic EXPLAIN

```sql
EXPLAIN SELECT * FROM cust_country WHERE country = 'USA';
```

#### Extended EXPLAIN (Required for Partition Details)

```sql
EXPLAIN EXTENDED SELECT * FROM cust_country WHERE country = 'USA';
```

Look for partition pruning information in the output:

```
partition values:
  country USA
```

#### Homework Questions and Answers

**Q: Which EXPLAIN command was required to view partition-related details?**

**A:** `EXPLAIN EXTENDED` — The extended version provides detailed information about partition pruning, showing which specific partitions will be scanned.

**Q: Why is partitioning so important for query performance?**

**A:** Partitioning improves query performance through **partition pruning** (also called partition elimination). When a query includes a filter on the partition column (e.g., `WHERE country = 'USA'`), Hive reads only the relevant partition directory instead of scanning the entire table. This dramatically reduces:

- I/O operations (fewer files to read)
- Processing time (less data to scan)
- Resource consumption (memory, CPU)

For large tables with billions of rows, partitioning can reduce query time from hours to seconds.

---

### Step 9: Examine HDFS Directory Structure

Exit Beeline and use the HDFS CLI:

```bash
hdfs dfs -ls /user/hive/warehouse/classicmodels.db/cust_country
```

#### Expected Output

```
drwxr-xr-x   - hive supergroup    0 ... /user/hive/warehouse/classicmodels.db/cust_country/country=Australia
drwxr-xr-x   - hive supergroup    0 ... /user/hive/warehouse/classicmodels.db/cust_country/country=France
drwxr-xr-x   - hive supergroup    0 ... /user/hive/warehouse/classicmodels.db/cust_country/country=Spain
drwxr-xr-x   - hive supergroup    0 ... /user/hive/warehouse/classicmodels.db/cust_country/country=USA
...
```

#### View Contents of a Partition Directory

```bash
hdfs dfs -ls /user/hive/warehouse/classicmodels.db/cust_country/country=USA
```

Expected output:

```
-rw-r--r--   1 hive supergroup    ... /user/hive/warehouse/classicmodels.db/cust_country/country=USA/000000_0
```

#### Homework Questions and Answers

**Q: What are the contents of the main directory for this table?**

**A:** The main directory (`/user/hive/warehouse/classicmodels.db/cust_country`) contains **subdirectories** for each partition value. Each subdirectory is named using the format `partition_column=value` (e.g., `country=USA`, `country=France`).

**Q: What are the names of the subdirectories?**

**A:** The subdirectories follow the naming convention `country=<value>`:

- `country=USA`
- `country=France`
- `country=Spain`
- `country=Australia`
- (etc., depending on which countries appear in the first 50 rows)

Each subdirectory contains the actual data files (in AVRO format) for that partition.

---

## Summary: Partitioned Table Architecture

```
/user/hive/warehouse/classicmodels.db/cust_country/
├── country=Australia/
│   └── 000000_0          (AVRO data file)
├── country=France/
│   └── 000000_0          (AVRO data file)
├── country=Spain/
│   └── 000000_0          (AVRO data file)
├── country=USA/
│   └── 000000_0          (AVRO data file)
└── ...
```

---

## Key Concepts

### Partitioning vs Non-Partitioned Tables

| Aspect | Non-Partitioned | Partitioned |
|--------|-----------------|-------------|
| Directory structure | Single directory with all data | Subdirectories per partition value |
| Query with filter | Full table scan | Reads only matching partitions |
| Insert complexity | Simple INSERT | Requires partition specification |
| Best for | Small tables, no common filter columns | Large tables filtered by specific columns |

### AVRO File Format

AVRO is a row-based storage format that provides:

- Schema evolution support
- Compact binary encoding
- Self-describing (schema embedded in file)
- Good for write-heavy workloads

---

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Need to specify partition columns` | Dynamic partitioning not enabled | Run `SET hive.exec.dynamic.partition=true;` |
| `Dynamic partition strict mode requires at least one static partition` | Default strict mode active | Run `SET hive.exec.dynamic.partition.mode=nonstrict;` |
| `MoveTask` errors | Environment-specific issue | Can be ignored per assignment instructions |
| Partition column in wrong position | Column order matters in INSERT | Ensure partition column is **last** in SELECT |

---

## Quick Reference: Complete Command Sequence

```sql
-- Step 1-2: Preview and analyze data
USE classicmodels;
SELECT * FROM customers LIMIT 20;
SELECT country, COUNT(*) AS cnt FROM customers GROUP BY country ORDER BY cnt DESC;

-- Step 3: Get DDL
SHOW CREATE TABLE customers;

-- Step 4: Create partitioned table
CREATE TABLE cust_country (
  customernumber INT,
  customername STRING,
  contactlastname STRING,
  contactfirstname STRING,
  phone STRING,
  addressline1 STRING,
  addressline2 STRING,
  city STRING,
  state STRING,
  postalcode STRING,
  salesrepemployeenumber INT,
  creditlimit DOUBLE
)
PARTITIONED BY (country STRING)
STORED AS AVRO;

-- Step 5: Verify
DESCRIBE FORMATTED cust_country;

-- Step 6: Enable dynamic partitioning and insert data
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO TABLE cust_country
PARTITION (country)
SELECT 
  customernumber, customername, contactlastname, contactfirstname,
  phone, addressline1, addressline2, city, state, postalcode,
  salesrepemployeenumber, creditlimit, country
FROM customers
LIMIT 50;

-- Step 7: Query partitioned data
SELECT * FROM cust_country WHERE country = 'USA';

-- Step 8: Examine execution plan
EXPLAIN EXTENDED SELECT * FROM cust_country WHERE country = 'USA';

-- Step 9: Check partitions
SHOW PARTITIONS cust_country;
```

```bash
# HDFS commands
hdfs dfs -ls /user/hive/warehouse/classicmodels.db/cust_country
hdfs dfs -ls /user/hive/warehouse/classicmodels.db/cust_country/country=USA
```