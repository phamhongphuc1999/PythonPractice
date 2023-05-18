from kafka import KafkaConsumer

if __name__ == "__main__":
    consumer = KafkaConsumer(bootstrap_servers=["localhost:9092"], auto_offset_reset="earliest")
    print(consumer.config)
    print(consumer.bootstrap_connected())
    consumer.subscribe(["quickstart-events"])

    for event in consumer:
        print(event)
