import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from typing import List, Dict, Any, Generator


# Фикстуры

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с набором тестовых транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:03:18.123456",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258736616364091",
            "to": "Счет 99066364287803317845"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa 1952884635627909",
            "to": "Maestro 7010870499239262"
        },
        {
            "id": 615064773,
            "state": "EXECUTED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 78808375133947487327",
            "to": "Счет 74342583020137146360"
        }
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_without_currency() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями без валюты."""
    return [
        {
            "id": 1,
            "description": "Транзакция без валюты",
            "operationAmount": {
                "amount": "100.00"
            }
        },
        {
            "id": 2,
            "description": "Еще одна без валюты",
            "operationAmount": {
                "amount": "200.00"
            }
        }
    ]


@pytest.fixture
def transactions_without_description() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями без описания."""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "description": "",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 3,
            "description": "Есть описание",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"code": "USD"}
            }
        }
    ]


# ==================== ТЕСТЫ ДЛЯ filter_by_currency ====================

class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тест фильтрации по валюте USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 2
        for transaction in usd_transactions:
            assert transaction['operationAmount']['currency']['code'] == "USD"
        assert usd_transactions[0]['id'] == 939719570
        assert usd_transactions[1]['id'] == 142264268

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тест фильтрации по валюте RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 2
        for transaction in rub_transactions:
            assert transaction['operationAmount']['currency']['code'] == "RUB"
        assert rub_transactions[0]['id'] == 873106923
        assert rub_transactions[1]['id'] == 594226727

    def test_filter_by_currency_eur(self, sample_transactions):
        """Тест фильтрации по валюте EUR."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

        assert len(eur_transactions) == 1
        assert eur_transactions[0]['operationAmount']['currency']['code'] == "EUR"
        assert eur_transactions[0]['id'] == 615064773

    def test_filter_by_currency_not_found(self, sample_transactions):
        """Тест фильтрации по отсутствующей валюте."""
        gbp_transactions = list(filter_by_currency(sample_transactions, "GBP"))

        assert len(gbp_transactions) == 0

    def test_filter_by_currency_empty_list(self, empty_transactions):
        """Тест фильтрации для пустого списка."""
        result = list(filter_by_currency(empty_transactions, "USD"))

        assert result == []

    def test_filter_by_currency_missing_currency_field(self, transactions_without_currency):
        """Тест фильтрации при отсутствии поля currency."""
        result = list(filter_by_currency(transactions_without_currency, "USD"))

        assert result == []

    def test_filter_by_currency_is_iterator(self, sample_transactions):
        """Тест проверки, что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions, "USD")

        assert hasattr(result, '__next__')
        assert hasattr(result, '__iter__')

        # Проверка, что можно получить элементы через next()
        first = next(result)
        assert first['operationAmount']['currency']['code'] == "USD"

    def test_filter_by_currency_case_sensitive(self, sample_transactions):
        """Тест чувствительности к регистру."""
        result_upper = list(filter_by_currency(sample_transactions, "USD"))
        result_lower = list(filter_by_currency(sample_transactions, "usd"))

        assert len(result_upper) == 2
        assert len(result_lower) == 0

    def test_filter_by_currency_with_empty_currency_code(self, sample_transactions):
        """Тест фильтрации с пустым кодом валюты."""
        result = list(filter_by_currency(sample_transactions, ""))

        assert result == []

    @pytest.mark.parametrize("currency_code,expected_count", [
        ("USD", 2),
        ("RUB", 2),
        ("EUR", 1),
        ("GBP", 0),
        ("", 0),
    ])
    def test_filter_by_currency_parametrized(self, sample_transactions, currency_code, expected_count):
        """Параметризованный тест фильтрации по разным валютам."""
        result = list(filter_by_currency(sample_transactions, currency_code))

        assert len(result) == expected_count


# ==================== ТЕСТЫ ДЛЯ transaction_descriptions ====================

class TestTransactionDescriptions:
    """Тесты для генератора transaction_descriptions."""

    def test_transaction_descriptions_normal(self, sample_transactions):
        """Тест получения описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]
        assert descriptions == expected

    def test_transaction_descriptions_empty_list(self, empty_transactions):
        """Тест для пустого списка транзакций."""
        descriptions = list(transaction_descriptions(empty_transactions))

        assert descriptions == []

    def test_transaction_descriptions_missing_description(self, transactions_without_description):
        """Тест для транзакций без описания."""
        descriptions = list(transaction_descriptions(transactions_without_description))

        # Должна вернуться только транзакция с непустым описанием
        assert descriptions == ["Есть описание"]

    def test_transaction_descriptions_is_generator(self, sample_transactions):
        """Тест проверки, что функция возвращает генератор."""
        result = transaction_descriptions(sample_transactions)

        assert hasattr(result, '__next__')
        assert hasattr(result, '__iter__')

        # Проверка получения через next()
        first = next(result)
        assert first == "Перевод организации"

    def test_transaction_descriptions_single_transaction(self):
        """Тест с одной транзакцией."""
        transactions = [
            {"description": "Одна транзакция"}
        ]
        descriptions = list(transaction_descriptions(transactions))

        assert descriptions == ["Одна транзакция"]

    def test_transaction_descriptions_all_empty_descriptions(self):
        """Тест с транзакциями, у которых все описания пустые."""
        transactions = [
            {"description": ""},
            {"description": ""},
            {"description": ""}
        ]
        descriptions = list(transaction_descriptions(transactions))

        assert descriptions == []

    def test_transaction_descriptions_mixed(self):
        """Тест со смешанными транзакциями."""
        transactions = [
            {"description": "Описание 1"},
            {"description": ""},
            {"description": "Описание 3"},
            {"id": 4},  # Без описания
            {"description": "Описание 5"}
        ]
        descriptions = list(transaction_descriptions(transactions))

        assert descriptions == ["Описание 1", "Описание 3", "Описание 5"]

    @pytest.mark.parametrize("transactions,expected", [
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{"description": ""}, {"description": "C"}], ["C"]),
        ([], []),
        ([{"description": "D"}], ["D"]),
    ])
    def test_transaction_descriptions_parametrized(self, transactions, expected):
        """Параметризованный тест с разными наборами транзакций."""
        result = list(transaction_descriptions(transactions))

        assert result == expected


# ==================== ТЕСТЫ ДЛЯ card_number_generator ====================

class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    def test_card_number_generator_small_range(self):
        """Тест генерации номеров карт в маленьком диапазоне."""
        result = list(card_number_generator(1, 5))

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]
        assert result == expected

    def test_card_number_generator_range_with_overflow(self):
        """Тест генерации с переходом через разряд."""
        result = list(card_number_generator(9998, 10002))

        expected = [
            "0000 0000 0000 9998",
            "0000 0000 0000 9999",
            "0000 0000 0001 0000",
            "0000 0000 0001 0001",
            "0000 0000 0001 0002"
        ]
        assert result == expected

    def test_card_number_generator_large_numbers(self):
        """Тест генерации больших чисел."""
        result = list(card_number_generator(9999999999999990, 9999999999999995))

        expected = [
            "9999 9999 9999 9990",
            "9999 9999 9999 9991",
            "9999 9999 9999 9992",
            "9999 9999 9999 9993",
            "9999 9999 9999 9994",
            "9999 9999 9999 9995"
        ]
        assert result == expected

    def test_card_number_generator_single_number(self):
        """Тест генерации одного номера."""
        result = list(card_number_generator(1234567890123456, 1234567890123456))

        assert result == ["1234 5678 9012 3456"]

    def test_card_number_generator_is_generator(self):
        """Тест проверки, что функция возвращает генератор."""
        result = card_number_generator(1, 5)

        assert hasattr(result, '__next__')
        assert hasattr(result, '__iter__')

        # Проверка получения через next()
        first = next(result)
        assert first == "0000 0000 0000 0001"

    def test_card_number_generator_start_greater_than_end(self):
        """Тест ошибки при start > end."""
        with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного"):
            list(card_number_generator(10, 5))

    def test_card_number_generator_start_less_than_minimum(self):
        """Тест ошибки при start < 1."""
        with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(0, 5))

    def test_card_number_generator_end_greater_than_maximum(self):
        """Тест ошибки при end > 9999999999999999."""
        with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(1, 10000000000000000))

    def test_card_number_generator_both_invalid(self):
        """Тест ошибки при start и end вне допустимого диапазона."""
        with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(-5, -1))

    def test_card_number_generator_zero_start(self):
        """Тест ошибки при start = 0."""
        with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(0, 0))

    def test_card_number_generator_exact_minimum(self):
        """Тест с минимальным допустимым значением."""
        result = list(card_number_generator(1, 1))

        assert result == ["0000 0000 0000 0001"]

    def test_card_number_generator_exact_maximum(self):
        """Тест с максимальным допустимым значением."""
        result = list(card_number_generator(9999999999999999, 9999999999999999))

        assert result == ["9999 9999 9999 9999"]

    @pytest.mark.parametrize("start,end,expected_first,expected_last", [
        (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
        (100, 103, "0000 0000 0000 0100", "0000 0000 0000 0103"),
        (9999, 10002, "0000 0000 0000 9999", "0000 0000 0001 0002"),
        (1000000000000000, 1000000000000003,
         "0001 0000 0000 0000", "0001 0000 0000 0003"),
    ])
    def test_card_number_generator_parametrized(self, start, end, expected_first, expected_last):
        """Параметризованный тест разных диапазонов."""
        result = list(card_number_generator(start, end))

        assert result[0] == expected_first
        assert result[-1] == expected_last
        assert len(result) == end - start + 1

    def test_card_number_generator_formatting(self):
        """Тест правильности форматирования номеров карт."""
        result = list(card_number_generator(1234567890123456, 1234567890123458))

        expected = [
            "1234 5678 9012 3456",
            "1234 5678 9012 3457",
            "1234 5678 9012 3458"
        ]
        assert result == expected

    def test_card_number_generator_all_digits(self):
        """Тест, что все символы - цифры или пробелы."""
        for card in card_number_generator(1, 10):
            # Убираем пробелы и проверяем, что остались только цифры
            digits_only = card.replace(" ", "")
            assert digits_only.isdigit()
            assert len(card) == 19  # 16 цифр + 3 пробела
            # Проверяем формат: группы по 4 цифры
            groups = card.split()
            assert len(groups) == 4
            for group in groups:
                assert len(group) == 4
                assert group.isdigit()

    def test_card_number_generator_large_range_chunk(self):
        """Тест генерации части большого диапазона."""
        generator = card_number_generator(1, 100)

        # Берем только первые 10 элементов
        first_ten = [next(generator) for _ in range(10)]

        assert first_ten[0] == "0000 0000 0000 0001"
        assert first_ten[-1] == "0000 0000 0000 0010"
        assert len(first_ten) == 10
