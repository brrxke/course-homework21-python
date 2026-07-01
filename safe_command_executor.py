#!/usr/bin/env python3


import shlex
import subprocess

ALLOWED_COMMANDS = ["ls", "pwd", "date", "whoami"]


def run_command(user_input: str):
    parts = shlex.split(user_input)

    if not parts or parts[0] not in ALLOWED_COMMANDS:
        return None, f"Команда запрещена. Разрешены: {', '.join(ALLOWED_COMMANDS)}", 1

    result = subprocess.run(parts, capture_output=True, text=True, shell=False)
    return result.stdout, result.stderr, result.returncode


def main():
    print(f"Разрешённые команды: {', '.join(ALLOWED_COMMANDS)} (или 'exit')")

    while True:
        user_input = input("\nВведите команду: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        stdout, stderr, code = run_command(user_input)
        print(f"[код: {code}]", stdout or stderr or "(нет вывода)")


if __name__ == "__main__":
    main()
