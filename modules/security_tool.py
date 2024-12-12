class SecurityTool:
    def __init__(self):
        from portscan import Portscan
        from system_enumeration import SystemEnumeration
        from keylogger import Keylogger

        self.portscan_module = Portscan()
        self.system_enumeration_module = SystemEnumeration()
        self.keylogger_module = Keylogger()

