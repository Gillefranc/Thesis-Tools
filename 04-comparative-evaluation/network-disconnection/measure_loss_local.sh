LOAD_CSV_FILE="load_status_local.csv"
TIMESTAMP_FILE="/root/loadgen/timestamps.csv"

# Function to log load status
log_load_status() {
  while true; do
    # Get the current time in ISO 8601 format
    TIME=$(date -Is)

    # Check if the timestamp file exists and has been updated in the last second
    if [[ -f "$TIMESTAMP_FILE" ]]; then
      LAST_MODIFIED=$(stat -c %Y "$TIMESTAMP_FILE")
      CURRENT_TIME=$(date +%s)

      if ((CURRENT_TIME - LAST_MODIFIED <= 1)); then
        LOAD_STATUS=1
      else
        LOAD_STATUS=0
      fi
    else
      # File does not exist, mark load status as failure
      LOAD_STATUS=0
    fi

    # Append the time and status to the load CSV file
    echo "$TIME,$LOAD_STATUS" >>"$LOAD_CSV_FILE"

    # Wait for 1 second
    sleep 1
  done
}

log_load_status &

wait
