#!/bin/bash

NODE_CSV_FILE="node_status.csv"

EDGE_SSH=...
KUBECONFIG=~/.kube/config

if [ ! -f "$NODE_CSV_FILE" ]; then
  echo "timestamp,value" >"$NODE_CSV_FILE"
fi

scp ./connection_loss.sh $EDGE_SSH:/root/
scp ./measure_loss_local.sh $EDGE_SSH:/root/

# Function to log node status
log_node_status() {
  while true; do
    TIME=$(date -Is)

    NODE_STATUS=$(kubectl --kubeconfig $KUBECONFIG get no | grep ubuntu | awk '{print $2}')

    echo "$TIME,$NODE_STATUS" >>"$NODE_CSV_FILE"

    sleep 1
  done
}

ssh $EDGE_SSH -t "/root/connection_loss.sh" &
ssh $EDGE_SSH -t "/root/measure_loss_local.sh" &

log_node_status &

wait

scp $EDGE_SSH:/root/load_status_local.csv .
