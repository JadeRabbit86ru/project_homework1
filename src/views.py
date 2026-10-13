from typing import Any


def print_operation(operation: dict[str, Any]) -> None:
    """Печатает одну операцию в требуемом формате."""
    date = operation.get("date", "")
    description = operation.get("description", "")

    # Отрезаем время от даты, если оно есть
    if "T" in str(date):
        date = str(date).split("T")[0]

    # Преобразуем дату из ISO в DD.MM.YYYY
    parts = str(date).split("-")
    if len(parts) == 3:
        date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
    else:
        date_str = str(date)

    print(f"{date_str} {description}")

    from_account = operation.get("from", "")
    to_account = operation.get("to", "")
    if from_account and to_account:
        print(f"{from_account} -> {to_account}")
    elif to_account:
        print(f"{to_account}")

    amount = operation.get("operationAmount", {})
    if isinstance(amount, dict):
        value = amount.get("amount", "")
        currency = amount.get("currency", {}).get("name", "")
        print(f"Сумма: {value} {currency}")
    print()
