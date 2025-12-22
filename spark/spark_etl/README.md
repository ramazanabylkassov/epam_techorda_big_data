# Restaurant & Weather Spark ETL

## Overview

This project implements a local Apache Spark ETL job that enriches restaurant
data with weather information based on geospatial proximity.  
The job is designed to run locally and follows best practices for data quality
checks, deterministic joins, and idempotent output.

---

## Input Data

### Restaurant Data
- Format: CSV
- Location: `data/input/restaurant_csv/`
- Structure: Multiple Spark-generated `part-*.csv` files
- Coordinates are provided using `lat` and `lng` columns

### Weather Data
- Format: Parquet
- Location: `data/input/weather_csv/`
- Partitioning: `year/month/day`
- Coordinates are provided using `lat` and `lng` columns

---

## Data Preparation Notes

### Weather Dataset Structure

The original weather dataset consisted of multiple independent Parquet
directories (e.g. `weather`, `weather 2`, `weather 3`, etc.), each with its own
partition root.

Apache Spark does not support reading multiple partition roots in a single
operation. To ensure correct partition discovery and stable reads, the weather
data was manually reorganized into a single Hive-style partitioned structure
(`year/month/day`) under the `weather_csv/` directory.

This allows Spark to read the weather data as one logical dataset and
automatically infer partition columns.

---

## Data Quality Checks

Restaurant records are checked for invalid coordinates:

- Records with `lat` or `lng` equal to `NULL` are identified and logged
- The number of invalid records is printed during execution

This satisfies the requirement to validate restaurant latitude and longitude
values prior to enrichment.

---

## Geohash Generation

A four-character geohash is generated from latitude and longitude using the
`geohash2` library.

- The same geohash logic is applied to both restaurant and weather datasets
- Geohash precision is fixed at 4 characters, as required

The generated geohash is stored in a new column named `geohash`.

---

## Join Strategy

To enrich restaurant data with weather information:

1. A four-character geohash is generated for both datasets
2. Weather data is **deduplicated by geohash** to prevent data multiplication
3. A **left join** is performed from restaurants to weather using the geohash

Duplicate coordinate columns (`lat`, `lng`) from the weather dataset are removed
after the join to ensure schema compatibility with Parquet output.

This approach guarantees:
- One output row per restaurant
- No row explosion
- Deterministic and repeatable results

---

## Idempotency

The ETL job is idempotent:

- Deterministic transformations are used
- Weather data is deduplicated prior to joining
- Output is written using `mode("overwrite")`

Running the job multiple times with the same input data produces identical
output.

---

## Output Data

- Format: Parquet
- Location: `output/enriched_restaurants/`
- Partitioning: `geohash`

The output contains all restaurant fields enriched with weather attributes and
is partitioned by geohash for efficient downstream access.

---

## Local Execution and Memory Configuration

During local execution, the job performs shuffle-intensive operations
(deduplication, join, and partitioned write).

To ensure stable execution on a local machine, additional memory was allocated
to Spark using the following command:

```bash
spark-submit --driver-memory 4g --executor-memory 4g etl_job.py
