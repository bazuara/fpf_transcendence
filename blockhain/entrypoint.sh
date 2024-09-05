#!/bin/bash

# Function to clean up the background Ganache process when the script exits
cleanup() {
    echo "Stopping Ganache..."
    kill $GANACHE_PID
    exit
}

# Trap CTRL+C and call the cleanup function
trap cleanup SIGINT

# Start Ganache in the background
echo "Starting Ganache..."
ganache-cli --quiet &

# Save the process ID of Ganache
GANACHE_PID=$!

# Wait for Ganache to be fully up
sleep 5

echo "Ganache is running with PID: $GANACHE_PID"

# Compile the Solidity contract using Truffle
echo "Compiling contracts..."
truffle compile > /dev/null 2>&1

# Deploy the contract to the running Ganache network
echo "Deploying contracts to Ganache..."
truffle migrate --network development | grep "contract address" | sed 's/^.*contract/contract/'

# Keep the script alive so the Ganache process is not terminated
# Press CTRL+C to stop both the script and Ganache
wait $GANACHE_PID
