import logging
from pathlib import Path

def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску номера карты в виде XXXX XX** **** XXXX"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает маску номера счета в виде **ХХХХ"""
    return "**" + account_number[-4:]


print("Какие-то изменения для коммита fix")

# Начало работы урок 12.2---------------------------------
# Создаём папку logs в корне проекта, если её нет
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Отдельный логер для модуля masks
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

# File handler с перезаписью файла при каждом запуске (mode="w")
masks_file_handler = logging.FileHandler(
    LOG_DIR / "masks.log", mode="w", encoding="utf-8"
)

# Формат: время - модуль - уровень - сообщение
masks_file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
masks_file_handler.setFormatter(masks_file_formatter)

# Устанавливаем handler для логера
masks_logger.addHandler(masks_file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Возвращает маску номера карты в виде XXXX XX** **** XXXX"""
    masks_logger.debug(
        f"Вызов get_mask_card_number с номером карты: {card_number}"
    )

    if (
        not isinstance(card_number, str)
        or len(card_number) != 16
        or not card_number.isdigit()
    ):
        masks_logger.error(
            f"Некорректный номер карты: {card_number}. Ожидается 16 цифр."
        )
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    masks_logger.info(f"Маска карты успешно сформирована: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Возвращает маску номера счета в виде **ХХХХ"""
    masks_logger.debug(
        f"Вызов get_mask_account с номером счёта: {account_number}"
    )

    if (
        not isinstance(account_number, str)
        or len(account_number) < 4
        or not account_number.isdigit()
    ):
        masks_logger.error(
            f"Некорректный номер счёта: {account_number}. "
            f"Ожидается минимум 4 цифры."
        )
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    masked = "**" + account_number[-4:]
    masks_logger.info(f"Маска счёта успешно сформирована: {masked}")
    return masked


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
