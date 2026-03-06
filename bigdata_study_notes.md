# Big Data Engineering — Study Notes
> Based on TechOrda / EPAM Big Data Masters Program Assessment Questions

---

## Table of Contents
1. [Introduction to Data & Big Data](#1-introduction-to-data--big-data)
2. [Hadoop & HDFS](#2-hadoop--hdfs)
3. [Hive](#3-hive)
4. [Spark](#4-spark)
5. [Kafka](#5-kafka)
6. [Elasticsearch & Elastic Stack](#6-elasticsearch--elastic-stack)
7. [Workflow Tools (Oozie, Airflow)](#7-workflow-tools-oozie-airflow)
8. [Data Movement & Streaming (NiFi)](#8-data-movement--streaming-nifi)
9. [Cloud & Hadoop in the Cloud](#9-cloud--hadoop-in-the-cloud)

---

## 1. Introduction to Data & Big Data

### What is Big Data?
Big Data refers to datasets that are too large, fast, or complex for traditional systems (like RDBMS) to handle. The goal is **storage and analysis of large-scale data**.

**Key characteristics (5 V's):**
- **Volume** — massive scale
- **Velocity** — high-speed generation
- **Variety** — structured, semi-structured, unstructured
- **Veracity** — data quality and trust
- **Value** — actionable insights

> 📌 **Exam question:** "Which describes the Big Data paradigm?" → *Storage and analysis of large-scale data*

### Big Data Sources
Common data sources include:
- **IoT systems** (sensors, devices)
- **Social media** (Twitter, Facebook)
- **Generic media** (images, audio, video)

> 📌 **Exam question:** All of the above are valid Big Data sources.

### Big Data Data Model
Big Data systems use a **flexible data model** — sometimes with no schema at all (schema-on-read), unlike relational databases which enforce a fixed schema upfront.

> 📌 **Exam question:** *"Flexible data model, sometimes with no schema at all"* best describes Big Data.

### Complex Data Types (MAP, ARRAY, STRUCT)
| Type | Use Case | Example |
|------|----------|---------|
| **MAP** | Key-value pairs | Phone labels: `{"Home": "555-1234", "Work": "555-5678"}` |
| **ARRAY** | Ordered list of same type | Tags: `["big data", "spark", "hive"]` |
| **STRUCT** | Named fields of different types | Address: `{city: "NY", zip: "10001"}` |

**Main benefit:** Eliminate joins by storing related data together in a single record.

> 📌 **Exam questions:**
> - Best type for address details (city, street, zip) → **Struct**
> - Best type for phone numbers with labels → **Map**
> - Main benefit of MAP/ARRAY → **Performance improvement, eliminating joins**

### AI-Driven Decision-Making
- Enables faster and more precise decisions
- Optimizes human resource allocation
- **Cannot** be done without data preparation

### 📚 Official Docs
- [Apache Hadoop Data Types](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types)

---

## 2. Hadoop & HDFS

### Hadoop Architecture Overview
Hadoop consists of:
- **HDFS** — distributed storage
- **YARN** — resource management
- **MapReduce** — processing framework

### HDFS Key Concepts

#### NameNode
The master node that manages the filesystem namespace.

**NameNode tasks:**
- Stores names and locations of HDFS blocks in the cluster
- Stores HDFS metadata **in RAM** for fast access
- Performs HDFS checkpoints (with Secondary NameNode)

> 📌 **Exam question:** Select all NameNode tasks → **storing block locations, storing metadata in RAM, performing checkpoints**

#### DataNode
- Stores actual data blocks
- Performs read/write operations from disk

#### Rack Awareness
- Nodes in the **same rack** have **higher** bandwidth than nodes in different racks
- Communication between nodes in **different racks** goes through network switches
- Rack-aware replica placement improves both **reliability** and **network efficiency**
- Replicas are placed on nodes from **different racks** for fault tolerance

> 📌 **Exam question:** Correct rack awareness statements → *"Communication between different rack nodes goes through switches"* and *"Replication happens on nodes from a different rack"*

#### HDFS Replication
- Default replication factor = 3
- One replica on the same node, one on a different node in the same rack, one on a different rack

#### HDFS Checkpoint
- Provides **high availability** in case of node failure
- Provides **data survivability** in case of storage failure
- Does NOT reduce stored data or provide geo-redundancy

> 📌 **Exam question:** Correct HDFS Checkpoint statements → **HA on node failure + data survivability on storage failure**

#### HDFS FSCK (File System Check)
- **Diagnoses** issues: missing files, corrupted/under-replicated blocks
- Does **NOT** automatically correct errors itself
- Does NOT lock files during scanning
- Can be run on a specific path (doesn't always scan everything)
- The **NameNode automatically corrects** most diagnosed issues (e.g., re-replication)

> 📌 **Exam question:** True regarding HDFS FSCK → *"It diagnoses issues"* + *"NameNode automatically corrects most issues"*

#### Data Locality
Moving **computation to data** rather than moving data over the network.

**Main benefit:** Increased performance as each node processes data stored locally.

> 📌 **Exam question:** Main benefit of Data Locality → **Increased performance as each node processes data stored locally**

### Hadoop File Types
| Format | Type | Best For |
|--------|------|----------|
| **Parquet** | Columnar | Analytics, aggregations |
| **ORC** | Columnar | Hive aggregations, optimized for Hive |
| **Avro** | Row-based | General-purpose row store, schema evolution |
| **SequenceFile** | Row-based binary | Binary data like images |
| **TextFile** | Row-based plain text | Simple/readable data |

> 📌 **Exam questions:**
> - Columnar file types → **Parquet and ORC**
> - Best for storing images → **SequenceFile**
> - Best general-purpose row store → **Avro**
> - Best for aggregations → **ORC (and Parquet)**
> - Best for random 10% sampling → **Buckets**

### Hadoop 3 vs Hadoop 2 Improvements
- **Erasure Coding** — reduces storage overhead
- **Intra-node balancing** — rebalancing within a node, not just cluster-level
- **High availability** — HDFS, YARN, Hive now support automatic failover
- **REST API** — enhanced monitoring and management
- **Scalability** — 10,000 node limit has been lifted

> 📌 **Exam question:** All 5 features above are Hadoop 3 improvements

### Hadoop Distributions
| Distribution | Notes |
|---|---|
| **Hortonworks (HDP)** | Merged with Cloudera → now **Cloudera Data Platform (CDP)** |
| **MapR** | Separate commercial distribution |
| **Apache** | Open-source baseline |
| **BigInsights** | IBM's distribution |

> 📌 **Exam question:** Which merged with Cloudera → **Hortonworks**

### Hadoop Management Tools (Cloudera Manager & Ambari)
**Benefits:**
- Easier management of cluster nodes and resources
- Easier troubleshooting of performance issues
- Automated alerts for performance conditions

**Ambari's main role:** Cluster administration

> 📌 **Exam question:** Main role of Ambari → **Cluster administration**

### Hadoop in AWS
| AWS Service | Hadoop Role |
|---|---|
| **S3** | Storage layer (replaces HDFS) |
| **EMR** | Processing layer (runs Hadoop/Spark) |

> 📌 **Exam questions:**
> - Hadoop storage layer in AWS → **S3**
> - Hadoop processing layer in AWS → **EMR**

### 📚 Official Docs
- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/current/)
- [HDFS Architecture](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [HDFS FSCK](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#fsck)

---

## 3. Hive

### Hive Overview
Hive is a data warehouse tool on top of Hadoop that provides SQL-like querying (HiveQL) over large datasets stored in HDFS.

### Hive Execution Engines
Hive supports three execution engines:
- **MapReduce** (original, slowest)
- **Tez** (faster, DAG-based)
- **Spark** (fastest, in-memory)

> 📌 **Exam question:** Valid Hive execution engines → **Tez, MapReduce, Spark** (not YARN, Mesos, HiveServer2)

### Hive Metastore
Stores:
- **Mapping of Hive tables to HDFS directories**
- Table schemas and partition information

Does NOT store:
- Block locations (that's NameNode)
- User privileges (that's Ranger/Sentry)

> 📌 **Exam question:** What is stored in Hive Metastore → **Mapping of Hive tables to HDFS directories**

### Managed vs External Tables
| Feature | Managed (Internal) | External |
|---------|-------------------|----------|
| Data ownership | Hive owns the data | Data owned externally |
| DROP TABLE | Deletes metadata + HDFS data | Deletes only metadata |
| Use case | Hive-controlled pipelines | Shared data sources |

> 📌 **Exam question:** What happens when we drop a managed table → **Both Metastore entry and HDFS data are deleted**

### Hive Joins
Hive supports all standard join types:
- **Inner Join**
- **Left Outer Join**
- **Full Outer Join**
- **Left Semi Join**
- **Cross Join**

> 📌 **Exam question:** All five join types are supported by Hive.

### Hive Partitioning
**Static partitioning:** Manually specify partition values when loading data.

**Dynamic partitioning:** Hive automatically creates partitions based on data values.
- NOT on by default
- Must set parameters **before inserting data**:
  ```sql
  SET hive.exec.dynamic.partition = true;
  SET hive.exec.dynamic.partition.mode = nonstrict;
  ```

> 📌 **Exam question:** How does Hive open new partitions → *"Can be created dynamically, requires setting parameters before inserting"* + *"Hive supports both static and dynamic partitioning"*

### Hive Bucketing
- Distributes data evenly using a hash function
- Best for **random sampling** (e.g., read 1 of 10 buckets to get 10% of data)
- Enables efficient **map-side joins** for bucketed tables

> 📌 **Exam question:** Most efficient structure for 10% random data → **Buckets**

### Hive Analytical / Window Functions
| Function | Purpose |
|----------|---------|
| `ROW_NUMBER()` | Sequential row number |
| `FIRST_VALUE()` | First value in window |
| `LAST_VALUE()` | Last value in window |
| `LEAD` | Next row's value |
| `LAG` | Previous row's value |
| `PERCENT_RANK` | Relative rank as percentage |

> 📌 **Exam question:** Locate date of first and last purchase per customer → **FIRST_VALUE()**

### Hive ANALYZE Command
```sql
ANALYZE TABLE tablename COMPUTE STATISTICS;
```
- **Collects statistics** and stores them in Hive Metastore
- Used by the query optimizer to improve execution plans

> 📌 **Exam question:** What is true about ANALYZE command → **Collects statistics and stores in Hive Metastore**

### Hive Transactional (ACID) Tables
Requirements to create a transactional table:
1. Set `"transactional=true"` table property
2. Must be an **INTERNAL (Managed)** table
3. Data must be in **ORC format**

**How ACID works:**
- UPDATE/DELETE create new **delta files** (don't modify existing files)
- Queries read both **base files + delta files** to show final result
- **Compaction** merges delta files to improve performance

**Minor vs Major Compaction:**
| Type | What it does |
|------|-------------|
| **Minor** | Merges many small delta files into one larger delta file |
| **Major** | Merges delta files INTO base files |

Both use MapReduce. Can be triggered manually with `ALTER TABLE ... COMPACT`.

**High compaction rate → improves query performance** (fewer files to scan)

> 📌 **Exam questions:**
> - Requirements for transactional table → **transactional=true + INTERNAL + ORC**
> - Minor compaction → **uses MapReduce, merges delta files into one, can use COMPACT command**

### Transaction/Lock Manager
Hive manages locks for transactional tables using **Zookeeper**.

> 📌 **Exam question:** Where does the Lock Manager manage locks → **Zookeeper service**

### Hive SerDe (Serializer/Deserializer)
When text file records are complex and can't be parsed by simple delimiters:
- Use a **Custom SerDe** with custom parsing logic

> 📌 **Exam question:** Complex non-trivial text file parsing → **Custom SerDe**

### Hive DELTA Construct (Incremental Updates)
The DELTA table in incremental update patterns:
- Should be an **INTERNAL (Managed)** table
- Should contain **updated or added records only** (not the full dataset)

> 📌 **Exam question:** DELTA construct attributes → **INTERNAL table + contains only updated/added records**

### Apache Impala
- Uses its own **MPP (massively parallel processing) execution engine**
- Stores **intermediate results in-memory** for speed
- Does NOT run on MapReduce or Spark
- Designed for **large-scale** data (not small/medium)
- Storage options: **HDFS, Amazon S3, HBase**

> 📌 **Exam questions:**
> - True regarding Impala → **stores results in-memory + uses own execution engine**
> - Storage options for Impala → **S3, HDFS, HBase**

### 📚 Official Docs
- [Apache Hive Documentation](https://hive.apache.org/)
- [Hive Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)
- [Hive Transactions (ACID)](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions)
- [Apache Impala](https://impala.apache.org/docs/build/html/topics/impala_intro.html)

---

## 4. Spark

### Spark Core Concepts

#### RDD (Resilient Distributed Dataset)
- Spark's **low-level** distributed data abstraction
- Supports **parallel processing** with a low-level API
- **Lazy evaluation** — transformations are not executed until an action is called
- Only supports **Transformations** and **Actions** (no "Terminals")

> 📌 **Exam questions:**
> - True for RDD → **supports parallel processing with low-level API**
> - Are Spark transformations eager? → **No, they are lazy**
> - Operation RDD does not support → **Terminals**

#### DataFrame
- Built on top of Dataset API (Spark 2.0+)
- Organizes data into **named columns**
- Available in **all languages** (Java, Scala, Python, R)
- In Scala/Java, `DataFrame = Dataset[Row]`

#### Dataset
- Strongly-typed version of DataFrame
- Available only in **Java and Scala** (not Python or R — no JVM type safety)
- Organizes data into named columns

> 📌 **Exam questions:**
> - Which organizes data into named columns → **DataFrame and Dataset (b and c)**
> - Dataset API available in which languages → **Java and Scala**
> - Not true for DataFrame → *"DataFrame is behind RDD"* (it's behind Dataset API)

### Transformations vs Actions
| Type | Description | Examples |
|------|-------------|---------|
| **Transformation** | Lazy, returns new RDD/DF | `map`, `filter`, `flatMap`, `zip`, `coalesce`, `repartition` |
| **Action** | Triggers execution, returns value | `count`, `collect`, `reduce`, `save` |

> 📌 **Exam questions:**
> - Which is NOT a transformation → **reduce** (it's an action)
> - What is an action → **counting the number of items**

### Key Transformations
| Transformation | Description |
|----------------|-------------|
| `map` | Apply function to each element |
| `filter` | Keep elements matching condition |
| `flatMap` | Map + flatten results |
| `zip` | Combine two RDDs by index position into key-value pairs |
| `repartition` | Change number of partitions (can increase OR decrease, causes full shuffle) |
| `coalesce` | Only decrease partitions (no full shuffle, more efficient) |

> 📌 **Exam questions:**
> - What does `zip` do → **combines two RDDs' corresponding elements**
> - Difference between coalesce and repartition → **repartition can increase partitions, coalesce cannot**

### SparkContext
- **Only ONE** SparkContext per Spark application
- Entry point for all Spark functionality

> 📌 **Exam question:** How many SparkContexts per application → **Only one**

### Spark SQL & Catalyst Optimizer
The Catalyst optimizer processes queries through these stages:
1. **Logical Plan** — parse and resolve the query
2. **Optimized Logical Plan** — apply optimizations (predicate pushdown, column pruning)
3. **Physical Plan** — generate possible physical execution strategies
4. **Optimized Physical Plan** — select best physical plan using cost-based optimizer

**Predicate Pushdown** happens at the **Optimized Logical Plan** stage.

**Optimal execution order:** `Scan → Filter → Join → Aggregate`

> 📌 **Exam questions:**
> - What makes Spark SQL faster than RDDs → **Cost-based optimizer**
> - Predicate pushdown stage → **Optimized logical plan**
> - Correct execution order → **Scan, Filter, Join, Aggregate**

### Cost-Based Optimizer (CBO) Statistics
CBO uses:
- **Row statistics** (average row length)
- **Column statistics** (number of distinct values)
- **Table statistics** (number of rows)

Does NOT use environment/hardware statistics.

### Spark Join Algorithms
| Algorithm | Description | Shuffle? |
|-----------|-------------|---------|
| **Broadcast join** | Sends small table to all nodes | **No shuffle** |
| **Sort-merge join** | Sorts both datasets then merges | Yes |
| **Shuffle hash join** | Hashes and shuffles data | Yes |

**Default join algorithm (Spark 2.3+): Sort-merge join**

> 📌 **Exam questions:**
> - Join that does NOT shuffle → **Broadcast join**
> - Default join algorithm → **Sort-merge join**

### Spark Streaming
- Processes data as **micro-batches** (not true event-based processing)
- Core abstraction: **DStream (Discretized Stream)** — a sequence of RDDs
- Supports both **RDDs and DataFrames**
- **Structured Streaming** is the newer API that replaced Spark Streaming

> 📌 **Exam questions:**
> - True regarding Spark Streaming → **supports RDDs+DataFrames, uses DStreams, uses micro-batches**
> - What are DStreams based on → **RDDs**

### Spark Cluster Schedulers
Spark supports: **Local, Standalone, YARN, Mesos, Kubernetes**

> 📌 **Exam question:** Supported cluster schedulers → **All of the above**

### Shared Variables
| Type | Description |
|------|-------------|
| **Broadcast variable** | Read-only variable cached on each node; should NOT be modified after broadcast |
| **Accumulator** | Write-only counter/sum; should only be updated inside **actions** |

Accumulator info can be obtained programmatically on the driver or via Spark UI.

> 📌 **Exam question:** All three statements about shared variables → **All are true**

### Spark Shell
- Runs on command line
- Allows **interactive** testing of Spark code
- Supports reading from many data sources

### Databricks
Built on **Apache Spark** — founded by the creators of Spark.

> 📌 **Exam question:** Core technology in Databricks → **Spark**

### 📚 Official Docs
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Spark RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Spark Streaming Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- [Catalyst Optimizer](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

---

## 5. Kafka

### Kafka Architecture Elements
Four core components:
1. **Topic** — category/feed where messages are published
2. **Producer** — writes messages to topics
3. **Consumer** — reads messages from topics
4. **Broker** — server that stores and manages message delivery

> 📌 **Exam question:** Kafka architecture elements → **Topic, Producer, Consumer, Broker**

### Kafka Broker
Main role: **Receive messages from producers, store them durably, serve them to consumers.**

> 📌 **Exam question:** Main role of Broker → **None of the above** (the options described it incorrectly)

### Kafka Topics & Partitions
**Main purpose of partitions:** Scale a topic across many servers for parallel producer writes and parallel consumer reads.

**Key partition rules:**
- Each partition is an append-only log
- Producers always write to the **end** of a partition
- Each message gets a **unique sequential offset ID**
- When a **message key is specified**, all messages with that key go to the **same partition** (hash-based routing)

> 📌 **Exam questions:**
> - Main purpose of partitions → **Scale topic across servers for parallel producers/consumers**
> - Outcome when message key is specified → **All messages with that key go to the same partition**
> - True for Kafka writes → **Producers write to end + every message gets unique sequential ID**

### Kafka Replication
- `--replication-factor 3` → creates **3 identical replicas** of each partition across brokers
- **Leader replica** — handles all R/W requests
- **Follower replica** — replicates from leader, stays up-to-date
- Every partition has **exactly one leader**; others are followers

> 📌 **Exam questions:**
> - `--replication-factor 3` outcome → **3 identical replicas placed across cluster**
> - Leader vs follower → **leader handles R/W, follower replicates**

### Kafka Message Durability (acks)
| Setting | Behavior |
|---------|----------|
| `acks=0` | Producer does NOT wait for any acknowledgment |
| `acks=1` | Leader writes to local log, responds without waiting for followers |
| `acks=all` | Leader waits for ALL in-sync replicas to acknowledge |

> 📌 **Exam question:** Correct acks definition → **First option** (acks=0 no wait, acks=1 local only, acks=all full ISR)

### Consumer Groups
- Consumers in a group **share partitions** — each partition assigned to one consumer
- Partitions are **divided among consumers** in the group for parallel processing
- No two consumers in the same group read from the same partition

> 📌 **Exam question:** How consumer groups and partitions work → **Consumer group works together, partitions divided among consumers**

### Kafka Connect
Purpose: **Make it easy to add data pipelines for streaming data between Kafka and other systems** (databases, file systems, search indexes) in a scalable and reliable way using pre-built connectors.

### Kafka Mirror Maker
A **stand-alone tool for copying data between two Apache Kafka clusters** — used for disaster recovery and geo-replication.

### Event Streaming Definition
Event streaming is:
- Capturing data in real-time from event sources in the form of streams
- Storing events durably for later retrieval
- Processing and reacting to event streams in real-time or retrospectively
- Routing event streams to different destination platforms

> 📌 **Exam question:** True statements about event streaming → **2nd, 3rd, 4th, 5th options** (NOT batch processing)

### 📚 Official Docs
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Connect](https://kafka.apache.org/documentation/#connect)
- [Kafka MirrorMaker](https://kafka.apache.org/documentation/#georeplication)

---

## 6. Elasticsearch & Elastic Stack

### Elastic Stack Components
| Component | Role |
|-----------|------|
| **Elasticsearch** | Search and analytics engine |
| **Kibana** | Dashboards and visualization |
| **Logstash** | Aggregating and transforming log data |
| **Beats** | Lightweight data shippers (collect logs/metrics from servers) |

**NOT part of Elastic Stack:** Prometheus (that's a separate monitoring tool)

> 📌 **Exam questions:**
> - What is Beats used for → **Centralizing logs and metrics collection from servers/devices**
> - NOT part of Elastic Stack → **Prometheus**

### Inverted Index
- Maps each **unique term** to the list of documents containing it
- Purpose: **Speeds up full-text search by mapping terms to documents**

> 📌 **Exam question:** Purpose of inverted index → **Speeds up full-text search by mapping terms to documents**

### Elasticsearch Indexing Process
Correct sequence: **Refresh → Commit → Merge**

Wait — the correct sequence per Elasticsearch internals:
1. Documents written to in-memory buffer
2. **Refresh** — moves buffer to new segment (makes searchable)
3. **Commit (Flush)** — fsync to disk for durability
4. **Merge** — background process combining small segments

> 📌 **Exam question:** Correct indexing sequence → **(debated in exam) Commit → Refresh → Merge**

### Elasticsearch Query Types
Valid query types:
- `term` query — exact match
- `terms` query — multiple exact matches
- `regexp` query — regular expression matching
- `range` query — numeric/date ranges
- `wildcard` query

**NOT a valid query type:** `infix query`

> 📌 **Exam question:** Query type that does NOT exist → **infix query**

### Elasticsearch Analyzers (Built-in)
- **Standard analyzer** — default, splits on whitespace/punctuation, lowercases
- **Whitespace analyzer** — splits only on whitespace
- **Ngram analyzer** — generates n-grams

**NOT built-in:** `emoji analyzer`

> 📌 **Exam question:** Built-in analyzers → **standard, whitespace, ngram**

### Elasticsearch Aggregation Types
| Type | Description |
|------|-------------|
| **Range aggregation** | Buckets documents into defined ranges |
| **Histogram aggregation** | Buckets by fixed intervals |
| **Cardinality aggregation** | Counts unique values (like COUNT DISTINCT) |

**NOT valid:** Median aggregation, Phrase aggregation

> 📌 **Exam question:** Valid aggregation types → **Range, Histogram, Cardinality**

### Elasticsearch Geo Queries
To enable geo queries, you must **explicitly define `geo_point` or `geo_shape` mapping** in the index.

> 📌 **Exam question:** Enable geo queries → **Define geo_point or geo_shape in index mapping**

### Elasticsearch Replicas
- Replicas are **copies of primary shards** for fault tolerance
- Replicas are **NEVER** placed on the same node as their primary shard
- Number of replicas **CAN be changed** after index creation (unlike primary shards)
- Replicas **improve read performance** by distributing read operations

> 📌 **Exam question:** True about replicas → **copies for fault tolerance + improve query performance**

### Nested Fields in Elasticsearch
- Nested objects are stored as **separate hidden documents** internally
- Must **explicitly define** `"type": "nested"` in mapping
- Must use the **nested query type** to query nested fields
- They are **NOT** automatically flattened (that's the `object` type)

> 📌 **Exam question:** Considerations for nested fields → **1st, 2nd, 3rd options**

### Bool Query Clauses
| Clause | Effect on Score |
|--------|----------------|
| `must` | Affects score, must match |
| `should` | Affects score, optional |
| `filter` | **Does NOT affect score**, yes/no matching only |
| `must_not` | Excludes documents, does not affect score |

> 📌 **Exam question:** Get documents without affecting scoring → **filter**

### 📚 Official Docs
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Elastic Stack Overview](https://www.elastic.co/elastic-stack)
- [Elasticsearch Aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)

---

## 7. Workflow Tools (Oozie, Airflow)

### Apache Oozie

#### Overview
- Framework to **specify a job or complex workflow of dependent jobs**
- Workflows defined in **XML** (not Python)
- Stores all job-related information in an **RDBMS** (Oracle, MySQL, PostgreSQL)
- Workflows are represented as **DAGs (Directed Acyclic Graphs)**

#### Key Features
- Supports custom extensions to its DSL
- Can **automatically retry and handle job failures**
- Workflows **CAN be parameterized**
- Integrates with multiple plugins

> 📌 **Exam questions:**
> - Where does Oozie store job info → **RDBMS (Oracle, MySQL, PostgreSQL)**
> - True statements about Oozie → **framework for workflows, custom extensions, auto-retry, DAG-based**

### Apache Airflow

#### Overview
A platform to programmatically author, schedule, and monitor workflows as DAGs.

#### Core Components
1. **Scheduler** — daemon that polls and triggers DAGs/tasks based on schedule
2. **Web Server** — Flask-based UI for monitoring and managing workflows
3. **Executor** — mechanism for executing tasks
4. **Workers** — nodes/processors that run the actual tasks

**NOT Airflow components:** Coordinator, Bundle (those are Oozie), Metastore (that's Hive), Connector

> 📌 **Exam questions:**
> - Main Airflow components → **Executor, Scheduler, Web Server**
> - True about Airflow components → **Scheduler polls DAGs, Webserver is Flask-based, Executors/Workers distinction**

#### Airflow Deployment Architectures
Two types:
1. **Single-node** — all components on one machine (dev/test)
2. **Multi-node** — distributed across multiple machines (production)

> 📌 **Exam question:** Airflow architecture divisions → **Two: single-node and multi-node**

### 📚 Official Docs
- [Apache Oozie Documentation](https://oozie.apache.org/docs/5.2.1/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)

---

## 8. Data Movement & Streaming (NiFi)

### Apache NiFi

#### Overview
A data integration tool for automating data flow between systems with a visual interface.

#### Key Features
- Supports **clustering** — multiple nodes processing different data in parallel
- Enables data fetching via **SFTP** from remote machines
- Guarantees **data lineage/provenance** tracking
- Supports **custom processors/plugins** (can extend beyond built-in processors)
- Can be deployed on **multiple servers** (not single-server only)

> 📌 **Exam questions:**
> - True about NiFi → **supports clustering + SFTP + data lineage**
> - NiFi cluster behavior → **Each message delivered at least once, order not guaranteed**

### Streaming Data Characteristics
- Generated **continuously** by data sources
- Has a **wide variety of sources** (IoT, social media, logs)
- Sent in **small sizes continuously** (NOT occasionally in large batches)
- Has **valuable information**

> 📌 **Exam question:** True about streaming data → **generated continuously + wide variety of sources**

### 📚 Official Docs
- [Apache NiFi Documentation](https://nifi.apache.org/docs.html)

---

## 9. Cloud & Hadoop in the Cloud

### Main Benefits of Cloud Deployment
- **Elasticity** — scale up/down on demand
- **De-coupling storage and compute** — terminate compute when not needed, keep cheap storage
- **Easier cluster management** — cloud providers handle infrastructure

**NOT guaranteed benefits:**
- Cloud is NOT always cheaper long-term
- Security is a **shared responsibility** (not solely cloud vendor's)

> 📌 **Exam questions:**
> - Best way to reduce cloud costs → **De-couple storage and compute**
> - Main benefits of cloud → **Elasticity + de-coupling + easier management**

### GCP Services for Big Data
| Service | Purpose |
|---------|---------|
| **Google Dataflow** | Managed ETL pipelines (batch + streaming, based on Apache Beam) |
| **Cloud Dataproc** | Managed Hadoop/Spark clusters |
| **Stackdriver (Cloud Operations)** | Monitoring and logging for GCP services |
| **Cloud Pub/Sub** | Messaging service |
| **GCS** | Object storage |

> 📌 **Exam questions:**
> - Managed ETL pipeline in GCP → **Google Dataflow**
> - Monitor Cloud Dataproc clusters → **Stackdriver**

### Databricks
- Web-based platform built on **Apache Spark**
- Founded by creators of Apache Spark

### 📚 Official Docs
- [Google Cloud Dataflow](https://cloud.google.com/dataflow/docs)
- [Google Cloud Dataproc](https://cloud.google.com/dataproc/docs)
- [Google Cloud Operations (Stackdriver)](https://cloud.google.com/stackdriver/docs)
- [AWS EMR Documentation](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [Databricks Documentation](https://docs.databricks.com/)

---

## Quick Reference Cheat Sheet

### "NOT" / "Does NOT" Questions
| Question Type | Answer |
|---|---|
| Join that performs NO shuffle | **Broadcast join** |
| Query type NOT in Elasticsearch | **infix query** |
| NOT part of Elastic Stack | **Prometheus** |
| NOT a Hive execution engine | YARN, Mesos, HiveServer2 |
| NOT a built-in ES analyzer | **emoji analyzer** |
| NOT a valid ES aggregation | Median, Phrase |
| Operation RDD does NOT support | **Terminals** |
| Spark transformation that is actually an action | **reduce()** |
| File type NOT columnar | Avro, SequenceFile, TextFile |

### Default Settings to Remember
| Setting | Default Value |
|---|---|
| Spark default join (2.3+) | **Sort-merge join** |
| HDFS replication factor | **3** |
| Hive dynamic partitioning | **OFF by default** |
| SparkContexts per app | **Only 1** |
| Spark transformations | **Lazy (not eager)** |

### Storage Recommendations
| Use Case | Best Format |
|---|---|
| General-purpose row store | **Avro** |
| Hive aggregations | **ORC** |
| Analytics/columnar queries | **Parquet or ORC** |
| Binary data / images | **SequenceFile** |
| Random sampling (10%) | **Bucketing** |

---

*Notes compiled from TechOrda / EPAM Big Data Masters Program 2025 Assessment*