import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

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

    def test_short_card_number(self):
        """Проверка работы функции с номером карты короче ожидаемой длины."""
        # Функция должна работать даже с короткими строками
        result = get_mask_card_number("123456")
        assert result == "1234 56** **** "

    def test_empty_string(self):
        """Проверка обработки пустой строки."""
        result = get_mask_card_number("")
        assert result == " ** **** "

    def test_missing_card_number(self):
        """Проверка обработки строки без номера карты (None)."""
        with pytest.raises(TypeError):
            get_mask_card_number(None)


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

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

    def test_short_account_number(self):
        """Проверка работы функции с номером счета меньше ожидаемой длины."""
        # Если номер короче 4 символов, функция вержет то что есть
        assert get_mask_account("123") == "**123"
        assert get_mask_account("12") == "**12"
        assert get_mask_account("1") == "**1"

    def test_empty_string(self):
        """Проверка обработки пустой строки."""
        assert get_mask_account("") == "**"

    def test_missing_account_number(self):
        """Проверка обработки отсутствующего номера счета (None)."""
        with pytest.raises(TypeError):
            get_mask_account(None)
