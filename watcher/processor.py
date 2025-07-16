import subprocess
import os
import time

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def run_command(command, description):
    log(f"🔹 {description}")
    log(f"   └─ Команда: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        log("   ✅ Успешно")
    except subprocess.CalledProcessError as e:
        log(f"   ❌ Ошибка при выполнении: {e}")
        log(f"   Вывод: {e.stdout}")
        log(f"   Ошибка: {e.stderr}")
        raise

def process_file(input_path):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    log(f"📥 Обработка файла: {filename}.ai")

    temp_svg = os.path.join("/tmp", f"{filename}.svg")
    output_svg = os.path.join(OUTPUT_DIR, f"{filename}_out.svg")
    output_pdf = os.path.join(OUTPUT_DIR, f"{filename}_out.pdf")

    # Шаг 1: .AI → .SVG
    run_command(
        ["inkscape", input_path, f"--export-plain-svg={temp_svg}"],
        "Конвертация .ai в .svg"
    )

    # Шаг 2: Дорисовка 1 мм по всем сторонам
    run_command(
        [
            "inkscape", temp_svg,
            "--actions=select-all;duplicate;move:-1mm,0;select-all;duplicate;move:1mm,0;select-all;duplicate;move:0,-1mm;select-all;duplicate;move:0,1mm",
            f"--export-plain-svg={output_svg}"
        ],
        "Дорисовка краёв (1 мм во все стороны) и экспорт .svg"
    )

    # Шаг 3: SVG → PDF (опционально)
    run_command(
        ["inkscape", output_svg, f"--export-filename={output_pdf}"],
        "Экспорт .pdf (по желанию)"
    )

    log(f"✅ Обработка завершена: {filename}\n— SVG → {output_svg}\n— PDF → {output_pdf}")