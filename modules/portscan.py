import socket
import threading
import subprocess
from datetime import datetime

class Portscan:
    def __init__(self, timeout=1, repo_path= "https://raw.githubusercontent.com/BlertaJashanica/Trojan-repo/main/data/"):
        self.timeout = timeout
        self.open_ports = []  # List of open ports
        self.lock = threading.Lock()  # Lock for thread-safe access to open_ports
        self.repo_path = repo_path  # Path to the cloned GitHub repository

    def scan_port(self, target_ip, port):
        """Scan a single port and add it to the list of open ports if it is open."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((target_ip, port))
                if result == 0:  # Port is open
                    with self.lock:  # Ensure thread-safe updates to the list
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

    def write_results(self, file_name="portscan.txt"):
        """Write scan results to a file in the cloned repository."""
        try:
            with open(f"{self.repo_path}/{file_name}", "w") as file:
                file.write("Scanning ports...\n")
                file.write(f"Open ports: {self.open_ports}\n")
            print(f"Results written to {self.repo_path}/{file_name}")
        except Exception as e:
            self.log_error(f"Error writing results: {e}")

    def push_to_github(self, file_name="portscan.txt"):
        """Pushes the results file to the cloned GitHub repository."""
        try:
            subprocess.run(["git", "-C", self.repo_path, "add", file_name], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", "Update port scan results"], check=True)
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
    # Path to the locally cloned GitHub repository
    repo_path = "./data"

    target_ip = "127.0.0.1"
    ports = range(20, 1025)
    result_file = "portscan.txt"

    portscan_tool = Portscan(repo_path=repo_path)

    print("Starting port scan...")
    open_ports = portscan_tool.scan(target_ip, ports)
    print(f"Scan complete. Open ports: {open_ports}")

    portscan_tool.write_results(result_file)

    print("Pushing results to GitHub...")
    portscan_tool.push_to_github(result_file)
