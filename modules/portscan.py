import socket
import threading
import json

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
