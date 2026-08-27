from typing import List, Dict, Iterator, Any, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.
    """
    return (transaction for transaction in transactions
            if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency_code)


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции (версия с генераторным выражением).
    """
    for transaction in transactions:
        if transaction.get('description'):
            yield transaction.get('description')


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение диапазона (включительно)
        end: Конечное значение диапазона (включительно)

    Yields:
        Номер карты в формате "XXXX XXXX XXXX XXXX"

    Raises:
        ValueError: Если start > end или значения выходят за допустимый диапазон
    """
    # Проверка корректности диапазона
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    if start < 1 or end > 9999999999999999:
        raise ValueError("Номера карт должны быть в диапазоне от 1 до 9999999999999999")

    current = start
    while current <= end:
        # Форматируем число в 16-значный строковый вид с ведущими нулями
        formatted = f"{current:016d}"
        # Добавляем пробелы после каждых 4 цифр
        card_number = f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
        yield card_number
        current += 1
