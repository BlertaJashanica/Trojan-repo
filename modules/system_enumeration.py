import socket
import platform
import psutil
import json
from datetime import datetime
from security_tool import SecurityTool


class SystemEnumeration(SecurityTool):
    def __init__(self):
        super().__init__()

    def gather_info(self):
        return {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "username": self.username,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        }

    def save_and_upload(self):
        system_info = self.gather_info()
        file_path = f"data/system_info_{self.username}_{self.current_time}.json"
        self.push_to_github(file_path, json.dumps(system_info, indent=4), "System info upload")


system_enum = SystemEnumeration()
system_enum.save_and_upload()
