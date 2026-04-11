def filter_by_state(transactions: list, state: str = "EXECUTED") -> list:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате."""
    return sorted(transactions, key=lambda item: item.get("date", ""), reverse=reverse)
