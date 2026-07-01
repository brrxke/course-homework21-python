#!/usr/bin/env python3

import json
import re
import sys

SCHEMA = {
    "id": int,
    "name": str,
    "email": str,
    "age": int,
}

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_json(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: файл не является корректным JSON ({e}).")
        sys.exit(1)


def validate_record(record, label: str) -> list:
    errors = []

    if not isinstance(record, dict):
        return [
            f"{label}: запись должна быть объектом (dict), получено {type(record).__name__}"
        ]

    for field, expected_type in SCHEMA.items():
        if field not in record:
            errors.append(f"{label}: отсутствует обязательное поле '{field}'")
            continue

        value = record[field]

        if expected_type is int and isinstance(value, bool):
            errors.append(f"{label}: поле '{field}' должно быть int, получено bool")
            continue

        if not isinstance(value, expected_type):
            errors.append(
                f"{label}: поле '{field}' должно быть {expected_type.__name__}, "
                f"получено {type(value).__name__}"
            )

    if "email" in record and isinstance(record["email"], str):
        if not EMAIL_PATTERN.match(record["email"]):
            errors.append(
                f"{label}: поле 'email' имеет некорректный формат ('{record['email']}')"
            )

    if (
        "age" in record
        and isinstance(record["age"], int)
        and not isinstance(record["age"], bool)
    ):
        if not (0 <= record["age"] <= 150):
            errors.append(
                f"{label}: поле 'age' вне допустимого диапазона (0-150): {record['age']}"
            )

    if (
        "id" in record
        and isinstance(record["id"], int)
        and not isinstance(record["id"], bool)
    ):
        if record["id"] < 0:
            errors.append(
                f"{label}: поле 'id' не может быть отрицательным: {record['id']}"
            )

    return errors


def print_report(total: int, all_errors: dict) -> None:
    valid_count = total - len(all_errors)

    print("\n=== Отчёт о валидации ===")
    print(f"Всего записей: {total}")
    print(f"Валидных записей: {valid_count}")
    print(f"Записей с ошибками: {len(all_errors)}\n")

    if not all_errors:
        print("Все записи прошли проверку успешно.")
        return

    for label, errors in all_errors.items():
        print(f"[{label}] найдено ошибок: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
        print()


def main():
    filename = input("Введите путь к JSON-файлу: ").strip() or "data.json"
    data = load_json(filename)

    if isinstance(data, list):
        records = data
    else:
        records = [data]

    all_errors = {}
    for i, record in enumerate(records, start=1):
        label = f"Запись {i}"
        record_errors = validate_record(record, label)
        if record_errors:
            all_errors[label] = record_errors

    print_report(len(records), all_errors)


if __name__ == "__main__":
    main()
