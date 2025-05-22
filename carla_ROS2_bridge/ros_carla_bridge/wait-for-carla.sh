#!/bin/bash

CARLA_HOST=${CARLA_HOST:-172.17.0.1}
CARLA_PORT=2000
RETRIES=10

echo "⏳ Waiting for CARLA server to become available at $CARLA_HOST:$CARLA_PORT..."

for i in $(seq 1 $RETRIES); do
    if timeout 1 bash -c "</dev/tcp/$CARLA_HOST/$CARLA_PORT" &>/dev/null; then
        echo "✅ CARLA server is up at $CARLA_HOST:$CARLA_PORT!"
        exit 0
    fi
    sleep 1
done

echo "❌ CARLA server did not become available in time at $CARLA_HOST:$CARLA_PORT"
exit 1

