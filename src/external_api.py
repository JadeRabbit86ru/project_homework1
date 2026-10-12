import os
from typing import Any
from typing import Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Базовый URL API (без параметров, параметры передадим отдельно)
EXCHANGE_RATES_API_URL = "https://api.apilayer.com/exchangerates_data/latest"

# Получаем ключ из .env файла
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты к рублю через Exchange Rates Data API.
    """
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте файл .env")

    # Формируем заголовки точно так, как показал сервис
    headers = {
        "apikey": API_KEY
    }

    # Формируем параметры запроса (base - ваша валюта, symbols - то, во что конвертируем)
    params = {
        "base": currency,
        "symbols": "RUB"
    }

    # Делаем GET-запрос
    response = requests.get(EXCHANGE_RATES_API_URL, headers=headers, params=params)

    # Если произошла ошибка (например, неверный ключ или лимит запросов), выбросим исключение
    response.raise_for_status()

    data = response.json()

    # Проверяем, что запрос успешен и курс RUB есть в ответе
    if data.get("success") and "rates" in data and "RUB" in data["rates"]:
        return float(data["rates"]["RUB"])

    raise ValueError(f"Не удалось получить курс для валюты {currency}. Ответ API: {data}")


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency_code = operation_amount.get("currency", {}).get("code", "RUB")

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code)
        return round(amount * rate, 2)

    raise ValueError(f"Неподдерживаемая валюта: {currency_code}")
