# Basic Hive Interaction Using Hue

This guide walks through the first homework task covering fundamental Hive operations using the Hue web interface.

## Environment Setup

### 1. Clone and Configure Docker Environment

Clone the Docker Hive repository:

```bash
git clone https://github.com/sergysta/docker-hive
cd docker-hive
```

### 2. Update Hue Service Configuration

Modify the `hue` service in `docker-compose.yml`:

```yaml
hue:
  <<: *common
  image: gethue/hue:20241231-140101
  ports:
    - "8888:8888"
  volumes:
    - ./conf/hue.ini:/usr/share/hue/desktop/conf/hue.ini
  depends_on:
    hive-metastore-postgresql:
      condition: service_healthy
```

### 3. Start the Docker Environment

```bash
docker-compose up -d
```

### 4. Access Hue

Navigate to [http://localhost:8888/hue/editor/?type=hive](http://localhost:8888/hue/editor/?type=hive) and log in with credentials: **admin/admin**

---

## Task Walkthrough

### Part 1: Database Operations

#### Show Available Databases

```sql
SHOW DATABASES;
```

#### Create the "classicmodels" Database

```sql
CREATE DATABASE IF NOT EXISTS classicmodels;
```

#### Show All Tables in the Database

```sql
SHOW TABLES IN classicmodels;
```

> **Note:** The `USE classicmodels;` command may not persist across queries in Hue. If `SELECT current_database();` returns 'default' instead of 'classicmodels', use explicit database references in your queries (e.g., `classicmodels.customers` instead of just `customers`).

---

### Part 2: Create Tables

The classicmodels database uses `\001` (Ctrl+A) as the field delimiter. This is Hive's default delimiter and ensures proper parsing of the uploaded data files.

#### Customers Table

```sql
CREATE EXTERNAL TABLE classicmodels.customers (
  customerNumber INT,
  customerName STRING,
  contactLastName STRING,
  contactFirstName STRING,
  phone STRING,
  addressLine1 STRING,
  addressLine2 STRING,
  city STRING,
  state STRING,
  postalCode STRING,
  country STRING,
  salesRepEmployeeNumber INT,
  creditLimit DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/customers';
```

#### Employees Table

```sql
CREATE EXTERNAL TABLE classicmodels.employees (
  employeeNumber INT,
  lastName STRING,
  firstName STRING,
  extension STRING,
  email STRING,
  officeCode STRING,
  reportsTo INT,
  jobTitle STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/employees';
```

#### Offices Table

```sql
CREATE EXTERNAL TABLE classicmodels.offices (
  officeCode STRING,
  city STRING,
  phone STRING,
  addressLine1 STRING,
  addressLine2 STRING,
  state STRING,
  country STRING,
  postalCode STRING,
  territory STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/offices';
```

#### Payments Table

```sql
CREATE EXTERNAL TABLE classicmodels.payments (
  customerNumber INT,
  checkNumber STRING,
  paymentDate STRING,
  amount DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/payments';
```

#### Order Details Table

```sql
CREATE EXTERNAL TABLE classicmodels.orderdetails (
  orderNumber INT,
  productCode STRING,
  quantityOrdered INT,
  priceEach DOUBLE,
  orderLineNumber INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/orderdetails';
```

#### Products Table

```sql
CREATE EXTERNAL TABLE classicmodels.products (
  productCode STRING,
  productName STRING,
  productLine STRING,
  productScale STRING,
  productVendor STRING,
  productDescription STRING,
  quantityInStock INT,
  buyPrice DOUBLE,
  MSRP DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE
LOCATION '/classicmodels.db/products';
```

---

### Part 3: Viewing Table Structure

#### Expand the Customers Table and View Columns/Data Types

```sql
DESCRIBE FORMATTED customers;
```

This command displays:
- Column names and their data types
- Table properties (storage format, location, etc.)
- SerDe information (serialization/deserialization)

---

### Part 4: Required Queries

#### Query 1: Select All Rows from Employees Table

```sql
SELECT * FROM classicmodels.employees;
```

#### Query 2: Fetch Only the First 10 Rows

```sql
SELECT * FROM classicmodels.employees LIMIT 10;
```

#### Query 3: Filtered and Sorted Employee Query

Requirements:
- Fetch employee ID, first name, and last name
- Employee number between 1002 and 1100
- Order by last name descending
- Limit to first 5 rows

```sql
SELECT 
  employeeNumber,
  firstName,
  lastName
FROM classicmodels.employees
WHERE employeeNumber BETWEEN 1002 AND 1100
ORDER BY lastName DESC
LIMIT 5;
```

#### Query 4: Employee Count per Job Title

```sql
SELECT 
  jobTitle,
  COUNT(*) AS num_employees
FROM classicmodels.employees
GROUP BY jobTitle
ORDER BY num_employees DESC;
```

#### Query 5: Export Query Output to Text File

```sql
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/emp_job_count'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT 
  jobTitle,
  COUNT(*) AS num_employees
FROM classicmodels.employees
GROUP BY jobTitle
ORDER BY num_employees DESC;
```

> **Note:** This writes to the local filesystem within the Docker container, not to HDFS.

---

### Part 5: Check HDFS Location of Employees Table

```sql
DESCRIBE FORMATTED classicmodels.employees;
```

Look for the `Location` field in the output:

```
Location: hdfs://namenode:8020/classicmodels.db/employees
```

---

### Part 6: HDFS Browse

#### Option A: Using Hue HDFS Browser

1. In Hue, navigate to the File Browser
2. Browse to `/classicmodels.db/employees`
3. Click on individual files to examine contents

#### Option B: Using CLI (if Hue HDFS browser is unavailable)

If ports 50070 and 50075 are not mapped, use the command line:

```bash
# List files in the employees directory
hdfs dfs -ls /classicmodels.db/employees

# View file contents
hdfs dfs -cat /classicmodels.db/employees/<filename>
```

#### File Readability Analysis

| Question | Answer |
|----------|--------|
| Is the file human-readable? | Partially. The data is stored as plain text, but fields are separated by `\001` (non-printable character), which may appear as special characters or be invisible. |
| Which Hive table property controls this? | `FIELDS TERMINATED BY '\001'` — This is the field delimiter specified in the `ROW FORMAT DELIMITED` clause during table creation. Using a visible delimiter like `,` or `\t` would make files more human-readable. |

---

## Key Concepts

### Field Delimiter (`\001`)

The `\001` character (Ctrl+A, ASCII SOH) is Hive's default field delimiter. It was chosen because:
- It rarely appears in actual data
- It prevents parsing issues with common characters like commas or tabs
- It's the standard for Hive's default LazySimpleSerDe

### External vs Managed Tables

The tables created above are **external tables** (`CREATE EXTERNAL TABLE`), meaning:
- Hive does not manage the underlying data files
- Dropping the table removes only the metadata, not the data
- Data location is explicitly specified via `LOCATION`

### STORED AS TEXTFILE

This specifies that data is stored in plain text format (as opposed to ORC, Parquet, etc.), making it human-readable but less efficient for large-scale queries.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hue HDFS browser not working | Ensure ports 50070 and 50075 are mapped in docker-compose.yml, or use CLI commands |
| Tables appear empty | Verify that data files exist in the HDFS location specified in the table definition |