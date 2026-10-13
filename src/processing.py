import re
from typing import Any


def filter_by_state(transactions: list, state: str = "EXECUTED") -> list:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате."""
    return sorted(transactions, key=lambda item: item.get("date", ""), reverse=reverse)

# Обновление 13.2-------------------------------------------------------------------------


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """
    Возвращает список операций, в описании которых встречается строка search.

    Поиск выполняется без учёта регистра с использованием библиотеки re.

    :param data: список словарей с данными о банковских операциях
    :param search: строка поиска
    :return: отфильтрованный список словарей
    """
    if not search:
        return list(data)

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: list[dict[str, Any]] = []

    for operation in data:
        description = str(operation.get("description", ""))
        if pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой из заданных категорий.

    Категория определяется по полю description.

    :param data: список словарей с данными о банковских операциях
    :param categories: список категорий операций
    :return: словарь {название категории: количество операций}
    """
    result: dict[str, int] = {category: 0 for category in categories}

    for operation in data:
        description = str(operation.get("description", ""))
        for category in categories:
            if description == category:
                result[category] += 1

    return result
