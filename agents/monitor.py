import os
import json
import psutil

server_name = os.getenv("SERVER_NAME")
required_keys = ["cpu_threshold", "ram_threshold", "disk_threshold", "maintenance"]

with open('../config/config.json') as f:
    config = json.load(f)
    
server_config = config.get(server_name, {}) # get server config

# check if keys in server config
for key in required_keys:
    if key not in server_config:
        print(f"[CONFIG ERROR] Missing key in the configuration file of {server_name} : {key}")
        exit(1)

if server_config.get("maintenance", False):
    print("Server is in maintenance mode. Exiting...")
    exit()

# check CPU usage
cpu_usage = psutil.cpu_percent()
if cpu_usage > server_config["cpu_threshold"]:
    # generate ticket
    print(f"[MONITORING ALERT] CPU usage is {cpu_usage}%, (>{server_config['cpu_threshold']}%)")

# check RAM usage
ram_usage = psutil.virtual_memory().percent
if ram_usage > server_config["ram_threshold"]:
    # generate ticket
    print(f"[MONITORING ALERT] RAM usage is {ram_usage}%, (>{server_config['ram_threshold']}%)")

# check disk usage (for all partitions)
disk_partitions = psutil.disk_partitions()
for partition in disk_partitions:
    disk_usage = psutil.disk_usage(partition.mountpoint).percent
    if disk_usage > server_config["disk_threshold"]:
        # generate ticket
        print(f"[MONITORING ALERT] Disk usage on {partition.mountpoint} is {disk_usage}%, (>{server_config['disk_threshold']}%)")