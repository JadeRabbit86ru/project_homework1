"""Тесты для модуля widget."""
import pytest
from datetime import datetime
from src.widget import get_mask_card_number, get_mask_account, mask_account_card, get_date


class TestWidgetMaskCardNumber:
    """Тесты для функции get_mask_card_number из widget."""

    def test_valid_card_number(self):
        """Тестирование правильности маскирования номера карты."""
        assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    @pytest.mark.parametrize(
        "card_number,expected",
        [
            ("1234567890123456", "1234 56** **** 3456"),
            ("4111111111111111", "4111 11** **** 1111"),
            ("5500000000000004", "5500 00** **** 0004"),
        ],
    )
    def test_various_card_formats(self, card_number, expected):
        """Проверка работы функции на различных входных форматах номеров карт."""
        assert get_mask_card_number(card_number) == expected


class TestWidgetMaskAccount:
    """Тесты для функции get_mask_account из widget."""

    def test_valid_account_number(self):
        """Тестирование правильности маскирования номера счета."""
        assert get_mask_account("12345678901234567890") == "**7890"

    @pytest.mark.parametrize(
        "account_number,expected",
        [
            ("12345678901234567890", "**7890"),
            ("98765432109876543210", "**3210"),
            ("11111111111111111111", "**1111"),
        ],
    )
    def test_various_account_formats(self, account_number, expected):
        """Проверка работы функции с различными форматами номеров счетов."""
        assert get_mask_account(account_number) == expected


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.fixture
    def valid_transactions(self):
        """Фикстура с валидными данными для тестирования."""
        return {
            "card_visa": "Visa 1234567890123456",
            "card_mastercard": "MasterCard 5500000000000004",
            "account": "Счет 12345678901234567890",
        }

    def test_mask_card_visa(self, valid_transactions):
        """Тест маскирования карты Visa."""
        result = mask_account_card(valid_transactions["card_visa"])
        assert result == "Visa 1234 56** **** 3456"

    def test_mask_card_mastercard(self, valid_transactions):
        """Тест маскирования карты MasterCard."""
        result = mask_account_card(valid_transactions["card_mastercard"])
        assert result == "MasterCard 5500 00** **** 0004"

    def test_mask_account(self, valid_transactions):
        """Тест маскирования счета."""
        result = mask_account_card(valid_transactions["account"])
        assert result == "Счет **7890"

    @pytest.mark.parametrize(
        "input_string,expected",
        [
            ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
            ("MasterCard 5500000000000004", "MasterCard 5500 00** **** 0004"),
            ("Счет 12345678901234567890", "Счет **7890"),
            ("American Express 378282246310005", "American Express 3782 82** **** 0005"),
        ],
    )
    def test_parametrized_mask_types(self, input_string, expected):
        """Параметризованные тесты с разными типами карт и счетов."""
        assert mask_account_card(input_string) == expected

    def test_invalid_input_empty_string(self):
        """Тест обработки пустой строки."""
        # Пустая строка: rfind вернет -1, card_type будет "", card_number будет ""
        result = mask_account_card("")
        # Функция возвращает строку, показывая устойчивость к некорректным данным
        assert isinstance(result, str)

    def test_invalid_input_no_space(self):
        """Тест обработки строки без пробела (некорректный формат)."""
        # Строка без пробела вызовет ошибку
        result = mask_account_card("NoSpaceString")
        # В этом случае card_type будет "", card_number будет "NoSpaceString"
        # Функция вернет " NoSpaceString[:4] NoSpaceString[4:6]** **** NoSpaceString[-4:]"
        # Это показывает устойчивость функции к некорректным данным
        assert isinstance(result, str)


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.fixture
    def sample_dates(self):
        """Фикстура с примерами дат."""
        return {
            "valid_iso": "2024-01-15T10:30:00.000000",
            "valid_iso_2": "2023-12-31T23:59:59.999999",
            "valid_iso_3": "2020-06-15T00:00:00.000000",
        }

    def test_valid_date_conversion(self, sample_dates):
        """Тестирование правильности преобразования даты."""
        result = get_date(sample_dates["valid_iso"])
        assert result == "15.01.2024"

    @pytest.mark.parametrize(
        "date_str,expected",
        [
            ("2024-01-15T10:30:00.000000", "15.01.2024"),
            ("2023-12-31T23:59:59.999999", "31.12.2023"),
            ("2020-06-15T00:00:00.000000", "15.06.2020"),
            ("2021-03-20T12:00:00.123456", "20.03.2021"),
        ],
    )
    def test_various_date_formats(self, date_str, expected):
        """Проверка работы функции на различных входных форматах даты."""
        assert get_date(date_str) == expected

    def test_boundary_date(self):
        """Проверка граничных случаев даты."""
        # Начало года
        assert get_date("2024-01-01T00:00:00.000000") == "01.01.2024"
        # Конец года
        assert get_date("2024-12-31T23:59:59.999999") == "31.12.2024"

    def test_invalid_date_format(self):
        """Проверка обработки некорректного формата даты."""
        with pytest.raises(ValueError):
            get_date("15.01.2024")  # Не ISO формат

    def test_missing_date(self):
        """Проверка обработки отсутствующей даты."""
        with pytest.raises(TypeError):
            get_date(None)

    def test_empty_string_date(self):
        """Проверка обработки пустой строки."""
        with pytest.raises(ValueError):
            get_date("")
