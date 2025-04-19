import os
import json
import psutil
import time
import datetime
import uuid

server_name = os.getenv("SERVER_NAME")
required_keys = ["cpu_threshold", "ram_threshold", "disk_threshold", "maintenance", "category"]

#### FUNCTIONS ####

# Function to generate ticket
def generate_ticket(server_name, message, metric_type, category):
    # severity based on category
    severity_map = {
        "PROD": "CRITICAL",
        "INFRA": "HIGH",
        "QUA": "MEDIUM",
        "DEV": "LOW"
    }
    
    severity = severity_map.get(category, "MEDIUM") # default severity
    
    # ticket data
    ticket_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "server_name": server_name,
        "message": message,
        "metric_type": metric_type,
        "severity": severity,
        "ticket_id": str(uuid.uuid4()) # random ticket id
    }
    
    os.makedirs("tickets", exist_ok=True)
    
    # write ticket to file
    ticket_filename = f"tickets/{server_name}_{metric_type}_{int(time.time())}.json"
    with open(ticket_filename, 'w') as f:
        json.dump(ticket_data, f, indent=4)
    
    return ticket_filename

#### MAIN ####

# get script directory to find config file
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(script_dir), 'config', 'config.json')

# load config
with open(config_path) as f:
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
    message = f"[MONITORING ALERT] CPU usage is {cpu_usage}%, (>{server_config['cpu_threshold']}%)"
    generate_ticket(server_name, message, "CPU", server_config["category"])

# check RAM usage
ram_usage = psutil.virtual_memory().percent
if ram_usage > server_config["ram_threshold"]:
    message = f"[MONITORING ALERT] RAM usage is {ram_usage}%, (>{server_config['ram_threshold']}%)"
    generate_ticket(server_name, message, "RAM", server_config["category"])

# check disk usage (for all partitions)
disk_partitions = psutil.disk_partitions()
for partition in disk_partitions:
    disk_usage = psutil.disk_usage(partition.mountpoint).percent
    if disk_usage > server_config["disk_threshold"]:
        message = f"[MONITORING ALERT] Disk usage on {partition.mountpoint} is {disk_usage}%, (>{server_config['disk_threshold']}%)"
        generate_ticket(server_name, message, f"DISK_{partition.mountpoint.replace(':', '').replace('\\', '_')}", server_config["category"])