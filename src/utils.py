import json
import os
from pathlib import Path
from typing import List, Dict, Any


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу с данными о транзакциях.

    Returns:
        Список словарей с данными о транзакциях.
        Возвращает пустой список, если файл пустой, содержит не список или не найден.
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError, IOError):
        return []
