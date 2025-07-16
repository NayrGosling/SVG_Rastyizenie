from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_file
import time
import os

INPUT_DIR = "/app/input"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        log(f"Событие: {event.event_type}, Путь: {event.src_path}")
        if event.src_path.lower().endswith(".ai"):
            filename = os.path.basename(event.src_path)
            log(f"📁 Новый файл обнаружен: {filename}")
            try:
                process_file(event.src_path)
            except Exception as e:
                log(f"❗ Ошибка при обработке {filename}: {e}")

def process_existing_files():
    log(f"📂 Проверка существующих файлов в {INPUT_DIR}")
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".ai"):
            file_path = os.path.join(INPUT_DIR, filename)
            log(f"📁 Обнаружен существующий файл: {filename}")
            try:
                process_file(file_path)
            except Exception as e:
                log(f"❗ Ошибка при обработке {filename}: {e}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        log(f"❌ Папка {INPUT_DIR} не существует")
        exit(1)
    log(f"📂 Содержимое {INPUT_DIR} при запуске: {os.listdir(INPUT_DIR)}")
    process_existing_files()  # Обрабатываем существующие файлы
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