def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    return f"**{account_number[-4:]}"


def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счета в строке"""
    if input_string.startswith("Счет "):
        account_number = input_string[5:]
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        last_space_index = input_string.rfind(" ")
        card_type = input_string[:last_space_index]
        card_number = input_string[last_space_index + 1 :]
        masked_number = get_mask_card_number(card_number)
        return f"{card_type} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой из формата ISO 8601 в формат ДД.ММ.ГГГГ
    """
    from datetime import datetime

    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
