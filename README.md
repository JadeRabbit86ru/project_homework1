# Проект по маскировке банковских данных

Модуль предоставляет функции для маскировки номеров банковских карт и счетов, а также для работы с банковскими операциями (фильтрация и сортировка).

## Установка

Клонируйте репозиторий:
```bash
git clone git@github.com:JadeRabbit86ru/project_homework1.git
```
## Использование

### Маскировка карты и счета

get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты.

Параметры:

card_number (str): номер карты (16 цифр)

Возвращает: строку с маской в формате XXXX XX** **** XXXX

Пример:

python
from masks import get_mask_card_number

masked = get_mask_card_number("1234567890123456")
print(masked)  # 1234 56** **** 3456
get_mask_account(account_number: str) -> str
Маскирует номер банковского счета.

Параметры:

account_number (str): номер счета

Возвращает: строку с маской в формате **XXXX

Пример:

python
from masks import get_mask_account

masked = get_mask_account("12345678901234567890")
print(masked)  # **7890
mask_account_card(input_string: str) -> str
Определяет тип входящей строки (карта или счет) и возвращает замаскированный номер.

Параметры:

input_string (str): строка вида "Visa Platinum 1234567890123456" или "Счет 12345678901234567890"

Возвращает: строку с замаскированным номером

Пример:

python
from masks import mask_account_card

# Для карты
result = mask_account_card("Visa Platinum 1234567890123456")
print(result)  # Visa Platinum 1234 56** **** 3456

# Для счета
result = mask_account_card("Счет 12345678901234567890")
print(result)  # Счет **7890

### Работа с датами

get_date(date_str: str) -> str
Преобразует дату из формата ISO 8601 в формат ДД.ММ.ГГГГ.

Параметры:

date_str (str): дата в формате "%Y-%m-%dT%H:%M:%S.%f"

Возвращает: строку с датой в формате "%d.%m.%Y"

Пример:

python
from masks import get_date

date = get_date("2024-03-28T10:30:00.123456")
print(date)  # 28.03.2024

### Фильтрация и сортировка операций

filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list
Фильтрует список операций по статусу.

Параметры:

list_dict (list): список словарей с операциями

state (str): статус для фильтрации (по умолчанию 'EXECUTED')

Возвращает: новый список с отфильтрованными операциями

Пример:

python
from processing import filter_by_state

operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-01'},
    {'id': 2, 'state': 'CANCELED', 'date': '2024-03-02'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2024-03-03'}
]

executed = filter_by_state(operations)
print(executed)  # [{'id': 1, ...}, {'id': 3, ...}]

canceled = filter_by_state(operations, 'CANCELED')
print(canceled)  # [{'id': 2, ...}]
sort_by_date(list_dict: list, reverse: bool = True) -> list
Сортирует список операций по дате.

Параметры:

list_dict (list): список словарей с операциями

reverse (bool): порядок сортировки:

True (по умолчанию) — по убыванию (сначала новые)

False — по возрастанию (сначала старые)

Возвращает: новый отсортированный список

Пример:

python
from processing import sort_by_date

operations = [
    {'id': 1, 'date': '2024-03-01T10:00:00.123456'},
    {'id': 2, 'date': '2024-03-03T10:00:00.123456'},
    {'id': 3, 'date': '2024-03-02T10:00:00.123456'}
]

sorted_desc = sort_by_date(operations)
print(sorted_desc)  # Сначала id=2, потом id=3, потом id=1

sorted_asc = sort_by_date(operations, reverse=False)
print(sorted_asc)  # Сначала id=1, потом id=3, потом id=2

### Обновление 11.1

## Новые функции

filter_by_currency - Фильтрует транзакции по заданной валюте.

Пример

transactions = [
    {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        },
        "description": "Платеж в долларах"
    },
    {
        "operationAmount": {
            "amount": "200.00",
            "currency": {"code": "EUR"}
        },
        "description": "Платеж в евро"
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction['description'])  # Выведет: Платеж в долларах


transaction_descriptions - Генератор, который возвращает описание каждой транзакции по очереди.

Пример:

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"id": 123},  # Без описания
    {"description": ""}  # Пустое описание
]

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)  # Выведет: Перевод организации, Перевод со счета на счет


card_number_generator - Генератор номеров банковских карт в заданном диапазоне.

Пример:

# Генерация первых 5 номеров
for card_number in card_number_generator(1, 5):
    print(card_number)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005

# Генерация с переходом через разряд
for card in card_number_generator(9998, 10002):
    print(card)
# Вывод:
# 0000 0000 0000 9998
# 0000 0000 0000 9999
# 0000 0000 0001 0000
# 0000 0000 0001 0001
# 0000 0000 0001 0002

## Новые тесты

TestFilterByCurrency: 9 тестов для функции filter_by_currency
TestTransactionDescriptions: 8 тестов для функции transaction_descriptions
TestCardNumberGenerator: 14 тестов для генератора card_number_generator

Тесты покрывают более 80% кода и включают:
Позитивные сценарии (успешная работа)
Негативные сценарии (обработка ошибок)
Крайние случаи (пустые списки, граничные значения)
Проверку типов (возвращаемые итераторы/генераторы)

Параметризованные тесты

## Автор

Jade_Rabbit

Манаенков Илья
