import socket
import threading

class Portscan:
    def __init__(self, timeout=1):
        self.timeout = timeout
        self.open_ports = []  # Lijst van open poorten
        self.lock = threading.Lock()  # Vergrendeling voor thread-veilige toegang tot open_ports

    def scan_port(self, target_ip, port):
        """Scan een enkele poort en voeg deze toe aan de lijst van open poorten als deze open is."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((target_ip, port))
                if result == 0:  # Poort is open
                    with self.lock:  # Zorg ervoor dat de lijst veilig wordt bijgewerkt in een multithreaded omgeving
                        self.open_ports.append(port)
        except Exception:
            pass

    def scan(self, target_ip, ports):
        """
        Scans the specified ports on a given target IP address using multiple threads.
        """
        threads = []
        
        # Start een nieuwe thread voor elke poort
        for port in ports:
            thread = threading.Thread(target=self.scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()

        # Wacht tot alle threads klaar zijn
        for thread in threads:
            thread.join()

        return self.open_ports

security_tool = Portscan()
# Voorbeeld van de Portscan module
target_ip = "127.0.0.1"
ports = range(20, 1025)
print("Scanning ports...")
open_ports = security_tool.portscan_module.scan(target_ip, ports)
print(f"Open ports: {open_ports}")

