import re
from datetime import datetime

DANGEROUS = ["eval", "exec", "os.system", "__import__"]
HISTORY_FILE = "commands_history.log"


def is_dangerous(command):
    for pattern in DANGEROUS:
        if pattern in command:
            return True
    return False


def sanitize(command):
    dangerous_chars = [";", "|", "&", "$", "`", ">", "<", "(", ")", "!", "#", "*", "?", "[", "]", "{", "}", "~", "\n", "\r"]
    for char in dangerous_chars:
        command = command.replace(char, "")
    return command


def save_command(command):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {command}\n")


def main():
    print("Введите команду (или 'exit' для выхода):")
    while True:
        cmd = input("> ").strip()
        if cmd.lower() == "exit":
            print("Выход.")
            break

        if is_dangerous(cmd):
            print(f"Опасная команда отклонена: {cmd}")
            continue

        cleaned = sanitize(cmd)
        if cleaned != cmd:
            print(f"Очищено: {cleaned}")

        save_command(cleaned)
        print(f"Сохранено: {cleaned}")


if __name__ == "__main__":
    main()
