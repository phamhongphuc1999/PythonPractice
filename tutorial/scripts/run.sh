#!/bin/sh

./venv/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --jars elasticsearch-hadoop-8.7.1/dist/elasticsearch-spark-30_2.12-8.7.1.jar main.py
