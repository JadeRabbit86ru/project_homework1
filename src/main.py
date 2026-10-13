from typing import Any, Callable

from src.utils import read_json_file, read_csv_file, read_xlsx_file
from src.processing import process_bank_search, process_bank_operations
from src.views import print_operation


VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def _ask_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя Да/Нет и возвращает bool."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'.")


def _choose_file() -> list[dict[str, Any]]:
    """Меню выбора источника данных."""
    print(
        "Привет! Добро пожаловать в программу работы\n"
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    readers: dict[str, Callable[[str], list[dict[str, Any]]]] = {
        "1": read_json_file,
        "2": read_csv_file,
        "3": read_xlsx_file,
    }
    paths: dict[str, str] = {
        "1": "data/operations.json",
        "2": "data/transactions.csv",
        "3": "data/transactions.xlsx",
    }
    names: dict[str, str] = {
        "1": "JSON-файл",
        "2": "CSV-файл",
        "3": "XLSX-файл",
    }

    while True:
        choice = input().strip()
        if choice in readers:
            print(f"Для обработки выбран {names[choice]}.")
            return readers[choice](paths[choice])
        print("Неверный пункт меню. Попробуйте снова.")


def _filter_by_status(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Запрашивает статус и фильтрует операции."""
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}"
        )
        status = input().strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return [
                op for op in data
                if str(op.get("state", "")).upper() == status
            ]
        print(f'Статус операции "{status}" недоступен.')


def _sort_by_date(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Спрашивает необходимость сортировки и её направление."""
    if not _ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        return data

    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ("по возрастанию", "возрастание", "asc"):
            return sorted(data, key=lambda op: str(op.get("date", "")))
        if order in ("по убыванию", "убывание", "desc"):
            return sorted(data, key=lambda op: str(op.get("date", "")), reverse=True)
        print("Введите 'по возрастанию' или 'по убыванию'.")


def _filter_rubles(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Оставляет только рублёвые транзакции, если пользователь согласен."""
    if not _ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        return data

    result: list[dict[str, Any]] = []
    for op in data:
        amount = op.get("operationAmount", {})
        if isinstance(amount, dict):
            currency = amount.get("currency", {})
            if isinstance(currency, dict) and currency.get("name") == "руб.":
                result.append(op)
    return result


def _filter_by_word(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Фильтрует по слову в описании через process_bank_search."""
    if not _ask_yes_no(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
    ):
        return data

    search = input("Введите слово для поиска в описании: ").strip()
    return process_bank_search(data, search)


def main() -> None:
    """Точка входа: связывает все шаги обработки."""
    data = _choose_file()
    data = _filter_by_status(data)
    data = _sort_by_date(data)
    data = _filter_rubles(data)
    data = _filter_by_word(data)

    print("Распечатываю итоговый список транзакций...\n")

    if not data:
        print(
            "Не найдено ни одной транзакции, подходящей под ваши\n"
            "условия фильтрации"
        )
        return

    print(f"Всего банковских операций в выборке: {len(data)}\n")
    for operation in data:
        print_operation(operation)


if __name__ == "__main__":
    main()
