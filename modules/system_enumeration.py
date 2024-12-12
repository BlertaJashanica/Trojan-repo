# system_enumeration.py

import socket
import platform
import psutil
from datetime import datetime
import os 

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

security_tool = SystemEnumeration()
# Voorbeeld van de System Enumeration module
print("Gathering system information...")
system_info = security_tool.system_enumeration_module.gather_info()
print(json.dumps(system_info, indent=4))
