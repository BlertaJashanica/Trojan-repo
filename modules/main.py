# main.py

import time
import json
from security_tool import SecurityTool

# Maak een instantie van de hoofdklasse
security_tool = SecurityTool()

# Voorbeeld van de Portscan module
target_ip = "127.0.0.1"
ports = range(20, 1025)
print("Scanning ports...")
open_ports = security_tool.portscan_module.scan(target_ip, ports)
print(f"Open ports: {open_ports}")

# Voorbeeld van de System Enumeration module
print("Gathering system information...")
system_info = security_tool.system_enumeration_module.gather_info()
print(json.dumps(system_info, indent=4))

# Voorbeeld van de Keylogger module
print("Starting keylogger (run for 10 seconds)...")
security_tool.keylogger_module.start()

print("Keylogger is running... Press keys to test it.")

# Run de keylogger voor 10 seconden voor testdoeleinden
time.sleep(10)

# Stop de keylogger en beëindig het programma
security_tool.keylogger_module.stop()
