import socket
import json
import threading
from test_main import SecurityTool


class Portscan(SecurityTool):
    def __init__(self, timeout=1):
        super().__init__()
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, target_ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
        except Exception:
            pass

    def scan(self, target_ip, ports):
        threads = []
        for port in ports:
            thread = threading.Thread(target=self.scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return self.open_ports

    def save_and_upload(self, target_ip):
        data = {"target_ip": target_ip, "open_ports": self.open_ports}
        file_path = f"data/portscan_{self.username}_{self.current_time}.json"
        self.push_to_github(file_path, json.dumps(data, indent=4), "Portscan results")


portscan = Portscan()
open_ports = portscan.scan("127.0.0.1", range(20, 1025))
portscan.save_and_upload("127.0.0.1")
