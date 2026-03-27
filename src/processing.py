def filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [item for item in list_dict if item.get('state') == state]


def sort_by_date(list_dict: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате."""
    return sorted(list_dict, key=lambda item: item.get('date', ''), reverse=reverse)
