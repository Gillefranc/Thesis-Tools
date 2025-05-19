#!/bin/bash

PROCESS_NAME="/root/fledge"

START_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR="/root/data/$START_TIME"

mkdir -p $OUTPUT_DIR

# Output CSV files
CPU_FILE="$OUTPUT_DIR/cpu.csv"
MEMORY_FILE="$OUTPUT_DIR/memory.csv"
NETWORK_FILE="$OUTPUT_DIR/network.csv"

# Write CSV headers
echo 'timestamp,value' >"$CPU_FILE"
echo 'timestamp,value' >"$MEMORY_FILE"

# Loop every second
while true; do
  # Find the PID of the process
  PID=$(pgrep -f "$PROCESS_NAME")

  if [ -z "$PID" ]; then
    echo "Process '$PROCESS_NAME' not found!"
    exit 1
  fi

  # Get CPU usage in percentage
  CPU_USAGE=$(ps -p $PID -o %cpu= | awk '{print $1}')

  # Get memory usage in MB
  MEMORY_USAGE_KB=$(awk '/VmRSS/{print $2}' /proc/$PID/status 2>/dev/null)
  MEMORY_USAGE_MB=$(echo "scale=2; $MEMORY_USAGE_KB / 1024" | bc)

  # Get current timestamp
  TIMESTAMP=$(date +"%H:%M:%S")

  # Append the data to the CSV files
  echo "$TIMESTAMP, $CPU_USAGE" >>"$CPU_FILE"
  echo "$TIMESTAMP, $MEMORY_USAGE_MB" >>"$MEMORY_FILE"

  # Wait for 1 second
  sleep 1
done
