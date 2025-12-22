from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import geohash2

spark = (
    SparkSession.builder
    .appName("Restaurant Weather ETL")
    .master("local[*]")
    .getOrCreate()
)

restaurants = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("data/input/restaurant_csv")
)

weather = spark.read.parquet("data/input/weather_csv")

restaurants.printSchema()
weather.printSchema()

invalid_coords = restaurants.filter(
    F.col("lat").isNull() | F.col("lng").isNull()
)

valid_coords = restaurants.filter(
    F.col("lat").isNotNull() & F.col("lng").isNotNull()
)

print("Invalid coordinate rows:", invalid_coords.count())

@F.udf("string")
def geohash4(lat, lon):
    if lat is None or lon is None:
        return None
    return geohash2.encode(lat, lon, precision=4)

restaurants_geo = restaurants.withColumn(
    "geohash",
    geohash4(F.col("lat"), F.col("lng"))
)

weather_geo = weather.withColumn(
    "geohash",
    geohash4(F.col("lat"), F.col("lng"))
)

weather_dedup = weather_geo.dropDuplicates(["geohash"])

enriched = (
    restaurants_geo
    .join(weather_dedup, on="geohash", how="left")
    .drop(weather_dedup["lat"])
    .drop(weather_dedup["lng"])
)

(
    enriched
    .write
    .mode("overwrite")
    .partitionBy("geohash")
    .parquet("output/enriched_restaurants")
)
