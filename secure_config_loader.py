#!/usr/bin/env python3

import json
import sys

CONFIG_FILE, ALLOWED_MODES, REQUIRED = (
    "config.json",
    ["development", "production", "testing"],
    ["port", "timeout", "mode"],
)


def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки '{filename}': {e}")
        sys.exit(1)


def validate_config(config):
    if not isinstance(config, dict):
        return [f"Конфигурация должна быть объектом, получено {type(config).__name__}"]

    errors = []
    for f in REQUIRED:
        if f not in config:
            errors.append(f"Отсутствует обязательное поле '{f}'")

    if "port" in config:
        v = config["port"]
        if isinstance(v, bool) or not isinstance(v, int):
            errors.append(
                f"'port' должен быть целым числом, получен {type(v).__name__}"
            )
        elif not 1 <= v <= 65535:
            errors.append(f"'port' вне диапазона 1-65535: {v}")

    if "timeout" in config:
        v = config["timeout"]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            errors.append(f"'timeout' должен быть числом, получен {type(v).__name__}")
        elif v <= 0:
            errors.append(f"'timeout' должен быть > 0: {v}")

    if "mode" in config:
        v = config["mode"]
        if not isinstance(v, str):
            errors.append(f"'mode' должен быть строкой, получен {type(v).__name__}")
        elif v not in ALLOWED_MODES:
            errors.append(
                f"'mode'='{v}' недопустим. Разрешены: {', '.join(ALLOWED_MODES)}"
            )

    if "host" in config and (
        not isinstance(config["host"], str) or not config["host"].strip()
    ):
        errors.append("'host' должен быть непустой строкой")

    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append(
            f"'debug' должен быть true/false, получен {type(config['debug']).__name__}"
        )

    return errors


def load_secure_config(filename=CONFIG_FILE):
    config = load_json(filename)
    errors = validate_config(config)
    if errors:
        print(f"\n=== Конфигурация отклонена ({len(errors)} ошибок) ===")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("Конфигурация прошла проверку успешно.")
    return config


def main():
    cfg = load_secure_config()
    print("\n=== Загруженная конфигурация ===")
    for k, v in cfg.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
