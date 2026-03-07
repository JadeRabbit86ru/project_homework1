def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску номера карты в виде XXXX XX** **** XXXX"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает маску номера счета в виде **ХХХХ"""
    return "**" + account_number[-4:]


print('Какие-то изменения для коммита start2')
print('Какие-то изменения для коммита start3')