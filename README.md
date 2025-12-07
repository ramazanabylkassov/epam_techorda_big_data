# Big Data Course - EPAM x TechOrda

## Overview

This repository contains notes, assignments, and project work from the Big Data course provided by **EPAM** and sponsored by **TechOrda**.

## Course Focus

Learning to work with industry-standard Big Data tools and technologies:

- **Hadoop** — Distributed storage and processing framework (HDFS, MapReduce)
- **Hive** — SQL-based data warehouse for querying large datasets
- **Spark** — Fast, in-memory data processing engine

## Repository Structure

```
.
├── README.md
└── hive/
    ├── docker-compose.yml
    ├── hadoop-hive.env
    ├── README.md
    └── homework/
        ├── 1_task_hue.md
        ├── 2_task_beeline.md
        ├── 3_task_managed_external_tables.md
        ├── 4_task_partition.md
        └── 5_task_acid.md
```

## Environment Setup

Docker-based Hive environment. See [hive/README.md](hive/README.md) for detailed setup instructions.

```bash
cd hive
docker-compose up -d
```

**Access:**
- **Hue:** http://localhost:8888 (admin/admin)
- **Beeline:** `beeline -u jdbc:hive2://localhost:10000 -n hive`

## Acknowledgments

- **EPAM** — Course provider
- **TechOrda** — Sponsorship and support

---

*Course in progress*