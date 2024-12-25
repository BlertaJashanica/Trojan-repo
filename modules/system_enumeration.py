import socket
import platform
import psutil
from datetime import datetime
import os 
import json

class SystemEnumeration:
    def __init__(self):
        pass

    def gather_info(self):
        """
        Collects basic system information such as OS details, users, and running processes.
        """
        info = {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "username": os.environ.get("USER") or os.environ.get("USERNAME") or "Unknown",
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            # "running_processes": [p.info for p in psutil.process_iter(attrs=['pid', 'name'])]
        }
        return info

# Create an instance of the SystemEnumeration class
security_tool = SystemEnumeration()

# Gather system information
print("Gathering system information...")
system_info = security_tool.gather_info()

# Print the system information
print(json.dumps(system_info, indent=4))

# Write the system information to an output file
output_file = "system_info.txt"
with open(output_file, "w") as file:
    json.dump(system_info, file, indent=4)

print(f"System information has been saved to {output_file}.")
