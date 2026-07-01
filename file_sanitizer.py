#!/usr/bin/env python3

import os
import re
import shutil

SECURE_DIR = "./secure_uploads"
ALLOWED_EXTENSIONS = {".txt", ".log", ".md"}


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"(\.\.|[/\\~])", "", filename)
    return os.path.basename(cleaned).strip(". ")


def main():
    source_path = input("Путь к исходному файлу: ").strip()
    if not os.path.isfile(source_path):
        print("Файл не найден.")
        return

    filename = sanitize_filename(input("Имя для сохранения: ").strip())
    ext = os.path.splitext(filename)[1].lower()

    if not filename or ext not in ALLOWED_EXTENSIONS:
        print(
            f"Недопустимое имя или расширение. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        return

    os.makedirs(SECURE_DIR, exist_ok=True)
    destination = os.path.join(SECURE_DIR, filename)

    if os.path.commonpath(
        [os.path.realpath(SECURE_DIR), os.path.realpath(destination)]
    ) != os.path.realpath(SECURE_DIR):
        print("Небезопасный путь. Операция отменена.")
        return
    shutil.copy2(source_path, destination)
    print(f"Файл сохранён: {destination}")


if __name__ == "__main__":
    main()
