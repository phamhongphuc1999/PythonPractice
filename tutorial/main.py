from pyspark import SparkConf
from pyspark.sql import SparkSession

if __name__ == "__main__":
    conf = SparkConf()
    conf.setMaster("local[*]")
    conf.setAppName("test")
    spark: SparkSession = (
        SparkSession.builder.master("local[1]")
        .appName("my_app")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    raw_logs_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "messages")
        .option("startingOffsets", "earliest")
        .load()
    )
    query1 = raw_logs_df.writeStream.format("console").start()
    raw_logs_df.printSchema()
    query1.awaitTermination()
    print("Done!")
