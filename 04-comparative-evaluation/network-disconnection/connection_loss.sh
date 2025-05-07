#!/bin/bash

# Get a list of all network interfaces (excluding loopback lo)
INTERFACES=$(ip -o link show | awk -F': ' '{print $2}' | grep -v '^lo$')

echo "Disabling all network interfaces except loopback..."
for iface in $INTERFACES; do
  echo "Disabling interface $iface..."
  sudo ip link set $iface down
done

echo "Network disconnected for 180 seconds..."
sleep 180

echo "Re-enabling all network interfaces..."
for iface in $INTERFACES; do
  echo "Re-enabling interface $iface..."
  sudo ip link set $iface up
done

echo "Network restored."
