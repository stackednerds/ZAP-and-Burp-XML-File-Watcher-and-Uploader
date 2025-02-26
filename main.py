import os
import requests
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Global variables
TOKEN = ""  #DD_TOKEN
PRODUCT_NAME = "Zap"
ENGAGEMENT_NAME = "ZapScan"
DIRECTORY_TO_WATCH = "./"
TIMEOUT = 30  # Timeout in seconds
URL="" #DD_URL

class Watcher:
    def __init__(self, directory_to_watch):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch
        self.timer = None
        self.timer_active = False

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=False)
        self.observer.start()
        print(f"Watching directory: {self.directory_to_watch} for XML files")
        print(f"Will exit after {TIMEOUT} seconds if no new XML files are detected")
        try:
            # Start the initial timer
            self.start_timer()
            # Keep the main thread alive
            while self.observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def start_timer(self):
        print(f"Starting/Resetting timer for {TIMEOUT} seconds")
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(TIMEOUT, self.stop)
        self.timer.daemon = True
        self.timer.start()
        self.timer_active = True

    def stop(self):
        print("No new XML file detected within the timeout period. Stopping the watcher.")
        if self.timer:
            self.timer.cancel()
        self.observer.stop()
        self.timer_active = False
        os._exit(0)

class Handler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(".xml"):
            print(f"New XML file detected: {event.src_path}")
            # Reset timer as we just detected activity
            self.watcher.start_timer()
            upload_and_delete_file(event.src_path, self.watcher)

def upload_and_delete_file(file_path, watcher):
    url = URL+"/api/v2/import-scan/"
    headers = {
        "Authorization": f"Token {TOKEN}"
    }
    
    try:
        with open(file_path, "rb") as file_obj:
            files = {
                "scan_type": (None, "ZAP Scan"),
                "file": (os.path.basename(file_path), file_obj),
                "product_name": (None, PRODUCT_NAME),
                "engagement_name": (None, ENGAGEMENT_NAME),
                "auto_create_context": (None, "true"),
                "active": (None, "true"),
                "verified": (None, "true")
            }
            
            response = requests.post(url, headers=headers, files=files)
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        watcher.start_timer()
        return
    
    if response.status_code == 201:
        print(f"Successfully uploaded and processed file: {file_path}")
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete file {file_path}: {str(e)}")
    else:
        print(f"Failed to upload file: {file_path}, Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Don't stop here, continue watching for more files
    # Start/reset the timer
    watcher.start_timer()

if __name__ == "__main__":
    watcher = Watcher(DIRECTORY_TO_WATCH)
    watcher.run()
