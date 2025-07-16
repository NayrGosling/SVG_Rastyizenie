from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_file
import time
import os

INPUT_DIR = "/app/input"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".ai"):
            filename = os.path.basename(event.src_path)
            log(f"📁 Новый файл обнаружен: {filename}")
            try:
                process_file(event.src_path)
            except Exception as e:
                log(f"❗ Ошибка при обработке {filename}: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), path=INPUT_DIR, recursive=False)
    observer.start()
    log(f"🟢 Мониторинг папки запущен: {INPUT_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
