import json
import logging
import csv
import openpyxl
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

utils_file_handler = logging.FileHandler(
    LOG_DIR / "utils.log", mode="w", encoding="utf-8"
)
utils_file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
utils_file_handler.setFormatter(utils_file_formatter)
utils_logger.addHandler(utils_file_handler)


def load_transactions_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу с данными о транзакциях.

    Returns:
        Список словарей с данными о транзакциях.
        Возвращает пустой список, если файл пустой,
        содержит не список или не найден.
    """
    utils_logger.debug(f"Попытка загрузки транзакций из файла: {filepath}")

    try:
        path = Path(filepath)

        if not path.exists():
            utils_logger.error(f"Файл не найден: {filepath}")
            return []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            utils_logger.error(
                f"Данные в файле {filepath} не являются списком. "
                f"Получен тип: {type(data).__name__}"
            )
            return []

        utils_logger.info(
            f"Успешно загружено {len(data)} транзакций из файла {filepath}"
        )
        return data

    except json.JSONDecodeError as e:
        utils_logger.error(
            f"Ошибка декодирования JSON в файле {filepath}: {e}"
        )
        return []
    except (OSError, IOError) as e:
        utils_logger.error(
            f"Ошибка ввода-вывода при чтении файла {filepath}: {e}"
        )
        return []

# Обновление 13.2-------------------------------------------------------------------------


def read_json_file(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def read_csv_file(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return [dict(row) for row in reader]


def read_xlsx_file(path: str) -> list[dict[str, Any]]:
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h) for h in rows[0]]
    result: list[dict[str, Any]] = []
    for row in rows[1:]:
        result.append(dict(zip(headers, row)))
    return result
