import time
import random
import requests
import threading
from datetime import datetime
import os

CONFIG_FILE = "/data/config.txt"
TIMESTAMP_FILE = "/data/timestamps.csv"

# Initialize running states
running_states = {
    "memory": 0,
    "cpu": 0,
    "network": 0,
}

# Lock for thread-safe updates
task_lock = threading.Lock()


def read_config():
    config = {"memory_usage": 0, "cpu": False, "network": False}
    try:
        with open(CONFIG_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split("=")
                if key == "memory_usage":
                    config[key] = int(value)
                elif key in ("cpu", "network"):
                    config[key] = value.lower() == "true"
    except Exception as e:
        print(f"Error reading config: {e}")
    return config


def simulate_memory(memory_in_mb):
    global running_states
    memory = []
    try:
        with task_lock:
            running_states["memory"] = 1
        memory = ["x" * 1024 * 1024 for _ in range(memory_in_mb)]
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        with task_lock:
            running_states["memory"] = 0
        del memory


def simulate_cpu():
    global running_states
    try:
        with task_lock:
            running_states["cpu"] = 1
        while True:
            random.random() ** random.random()
    finally:
        with task_lock:
            running_states["cpu"] = 0


def simulate_network():
    global running_states
    try:
        with task_lock:
            running_states["network"] = 1
        while True:
            try:
                requests.get("https://www.example.com")
                time.sleep(random.uniform(0.5, 2))
            except Exception as e:
                print(f"Network error: {e}")
    finally:
        with task_lock:
            running_states["network"] = 0


def log_timestamp():
    if not os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "w") as f:
            f.write("Date,Memory,CPU,Network\n")

    while True:
        with open(TIMESTAMP_FILE, "a") as f:
            with task_lock:
                timestamp = datetime.now().isoformat()
                memory = running_states["memory"]
                cpu = running_states["cpu"]
                network = running_states["network"]
                f.write(f"{timestamp},{memory},{cpu},{network}\n")
        print(f"{timestamp} - Memory: {memory}, CPU: {cpu}, Network: {network}")
        time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=log_timestamp, daemon=True).start()

    while True:
        config = read_config()

        if config["memory_usage"] > 0 and running_states["memory"] == 0:
            memory_thread = threading.Thread(
                target=simulate_memory, args=(config["memory_usage"],), daemon=True
            )
            memory_thread.start()

        if config["cpu"] and running_states["cpu"] == 0:
            cpu_thread = threading.Thread(target=simulate_cpu, daemon=True)
            cpu_thread.start()

        if config["network"] and running_states["network"] == 0:
            network_thread = threading.Thread(target=simulate_network, daemon=True)
            network_thread.start()

        time.sleep(1)
