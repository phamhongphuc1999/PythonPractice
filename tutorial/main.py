from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions

re_host = "(^\S+\.[\S+\.]+\S+)"
re_time = "\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})]"
re_method_uri_protocol = '"(\S+)\s(\S+)\s*(\S*)"'
re_status = "\s(\d{3})\s"
re_content_size = "(\d+)$"
log_pattern = f"{re_host}\s-\s-\s{re_time}\s{re_method_uri_protocol}{re_status}{re_content_size}"


def get_spark_config():
    _conf = SparkConf()
    _conf.setMaster("local[*]")
    _conf.setAppName("spark-test-app")
    # https://www.elastic.co/guide/en/elasticsearch/hadoop/current/configuration.html
    _conf.set("es.nodes", "https://localhost")
    _conf.set("es.port", "9200")
    _conf.set("es.net.http.auth.user", "elastic")
    _conf.set("es.net.http.auth.pass", "es_bigdataproject")
    _conf.set("es.net.ssl", "true")
    _conf.set("es.nodes.resolve.hostname", "false")
    _conf.set("es.net.ssl.cert.allow.self.signed", "true")
    _conf.set("es.nodes.wan.only", "true")
    _conf.set("es.nodes.discovery", "false")
    return _conf


if __name__ == "__main__":
    conf = get_spark_config()
    spark: SparkSession = (
        SparkSession.builder.config(conf=conf)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    raw_logs_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:29092")
        .option("subscribe", "messages")
        .option("startingOffsets", "earliest")
        .load()
    )
    parsed_logs_df = raw_logs_df.select(
        functions.regexp_extract("value", re_host, 1).alias("host"),
        functions.regexp_extract("value", re_time, 1).alias("timestamp"),
        functions.regexp_extract("value", re_method_uri_protocol, 1).alias("method"),
        functions.regexp_extract("value", re_method_uri_protocol, 2).alias("endpoint"),
        functions.regexp_extract("value", re_method_uri_protocol, 3).alias("protocol"),
        functions.regexp_extract("value", re_status, 1).alias("status"),
        functions.regexp_extract("value", re_content_size, 1).alias("content_size"),
    )
    parsed_logs_df.printSchema()

    final_data = (
        parsed_logs_df.writeStream.option("checkpointLocation", "checkpoints")
        .option("es.resource", "spark_logs_analysis/log")
        .outputMode("append")
        .format("org.elasticsearch.spark.sql")
        .start("spark_logs_analysis")
    )
    final_data.awaitTermination()

    # query1 = parsed_logs_df.writeStream.format("console").start()
    # parsed_logs_df.printSchema()
    # query1.awaitTermination()
    # print("Done!")
