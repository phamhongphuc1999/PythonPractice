from kafka import KafkaProducer
import json

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers="10.0.2.15:4000", api_version=(0, 11, 5))
    print(producer.config)
    print(producer.bootstrap_connected())
    producer.send("quickstart-events", b"message one")
