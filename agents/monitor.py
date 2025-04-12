import json
import psutil
import os

server_name = os.getenv("SERVER_NAME")
required_keys = ["cpu_threshold", "ram_threshold", "disk_threshold", "maintenance"]

with open('config/config.json') as f:
    config = json.load(f)
    
server_config = config.get(server_name, {}) # Get server config

# Check keys in server config
for key in required_keys:
    if key not in server_config:
        print(f"[ERREUR CONFIG] Missing key in the configuration file of {server_name} : {key}")
        exit(1)

if server_config.get("maintenance", False):
    print("Server is in maintenance mode. Exiting...")
    exit()

# Check CPU, RAM, and disk usage
if psutil.cpu_percent() > server_config["cpu_threshold"]:
    # generate ticket
    pass