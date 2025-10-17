#!/bin/bash

# Kafka container name
KAFKA_CONTAINER="tweeeeedbt-kafka-1"
BROKER="localhost:9092"

# Topics you want to reset
TOPICS=("ipl_raw" "VerifiedUserCheck" "GeoLocation" "TeamSpecific" "VerifiedUserWindowedCount")

echo "🧹 Deleting old topics..."

for TOPIC in "${TOPICS[@]}"; do
    echo "⛔ Deleting topic: $TOPIC"
    docker exec -i $KAFKA_CONTAINER kafka-topics --bootstrap-server $BROKER --delete --topic $TOPIC 2>/dev/null || true
    sleep 1
done

echo "🛠️ Recreating topics..."

for TOPIC in "${TOPICS[@]}"; do
    echo "✅ Creating topic: $TOPIC"
    docker exec -i $KAFKA_CONTAINER kafka-topics --bootstrap-server $BROKER \
        --create --topic $TOPIC --partitions 1 --replication-factor 1
    sleep 1
done

echo "🚀 Kafka topics have been reset!"
