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

## Тестирование

Проект включает модульные тесты для проверки корректности работы всех функций.

### Запуск тестов

Для запуска тестов используйте pytest:

```bash
pytest tests/
```

Или с подробным выводом:

```bash
pytest tests/ -v
```

### Структура тестов

- `test_masks.py` — тесты для функций маскировки карт и счетов
- `test_processing.py` — тесты для функций фильтрации и сортировки операций
- `test_widget.py` — тесты для виджетов

# Обновление 11.2 от 15.09.2026

## Декоратор `log`

Модуль `src/decorators.py` содержит декоратор `log`, предназначенный для
автоматического логирования вызовов функций: их запуска, успешного
завершения, возвращаемого результата, а также возникающих ошибок вместе
с входными параметрами.

## Возможности

- Логирование **успешного** выполнения функции.
- Логирование **ошибок** с указанием типа исключения и входных аргументов.
- Гибкий вывод логов:
  - в **файл**, если указан параметр `filename`;
  - в **консоль**, если `filename` не задан.
- Сохранение метаданных оригинальной функции (`__name__`, `__doc__`)
  благодаря `functools.wraps`.
- Проброс исключения наружу — поведение функции не изменяется.

# Обновление 12.1 от 29.10.2026

## Новые модули

### Модуль `src/utils.py`

**Функция `load_transactions_from_json(filepath)`** — загружает список финансовых транзакций из JSON-файла.
- Возвращает список словарей с данными о транзакциях
- Если файл не найден, пустой, содержит не список или невалидный JSON — возвращает пустой список

### Модуль `src/external_api.py`

**Функция `get_exchange_rate(currency)`** — получает текущий курс валюты (USD или EUR) к рублю через внешнее API. При недоступности основного API автоматически переключается на резервный источник.

**Функция `convert_to_rubles(transaction)`** — возвращает сумму транзакции в рублях (float).
- Если валюта RUB — сумма возвращается без изменений
- Если валюта USD или EUR — выполняется конвертация через API по актуальному курсу
- Для неподдерживаемых валют выбрасывается `ValueError`

API-ключ для внешнего сервиса хранится в файле `.env` (переменная `EXCHANGE_RATES_API_KEY`).

## Новые тесты

### `tests/test_utils.py` — тесты функции `load_transactions_from_json`

| Тест | Что проверяет |
|------|---------------|
| `test_load_valid_json` | Корректная загрузка валидного JSON-файла со списком транзакций |
| `test_file_not_found` | Возврат пустого списка при отсутствии файла |
| `test_empty_file` | Возврат пустого списка для пустого файла |
| `test_file_contains_dict_not_list` | Возврат пустого списка, если в файле словарь, а не список |
| `test_file_contains_string_not_list` | Возврат пустого списка, если в файле строка |
| `test_invalid_json` | Возврат пустого списка при невалидном JSON |
| `test_empty_list` | Возврат пустого списка, если в файле пустой список `[]` |

### `tests/test_external_api.py` — тесты функций `get_exchange_rate` и `convert_to_rubles`

| Тест | Что проверяет |
|------|---------------|
| `test_get_exchange_rate_usd` | Получение курса USD к RUB через API (с Mock ответа) |
| `test_get_exchange_rate_eur` | Получение курса EUR к RUB через API (с Mock ответа) |
| `test_get_exchange_rate_api_error` | Выброс `ValueError` при ошибке ответа API |
| `test_convert_rub_transaction` | Транзакция в RUB возвращается без конвертации |
| `test_convert_usd_transaction` | Конвертация транзакции из USD в RUB (с Mock курса) |
| `test_convert_eur_transaction` | Конвертация транзакции из EUR в RUB (с Mock курса) |
| `test_convert_unsupported_currency` | Выброс `ValueError` для неподдерживаемой валюты |
| `test_convert_empty_transaction` | Возврат `0.0` для пустой транзакции |
| `test_convert_usd_rounding` | Округление результата конвертации до 2 знаков после запятой |

## Автор

Jade_Rabbit

Манаенков Илья
