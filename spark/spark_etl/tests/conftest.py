import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("Spark Test")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.catalogImplementation", "in-memory")
        .getOrCreate()
    )
    yield spark
    spark.stop()
