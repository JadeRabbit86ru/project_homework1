from unittest.mock import patch, MagicMock

import pytest

from src.external_api import convert_to_rubles, get_exchange_rate


class TestGetExchangeRate:

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_usd(self, mock_get):
        """Тест получения курса USD к RUB."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "base": "USD",
            "date": "2021-03-17",
            "rates": {"RUB": 73.5}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        rate = get_exchange_rate("USD")
        assert rate == 73.5
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_eur(self, mock_get):
        """Тест получения курса EUR к RUB."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "base": "EUR",
            "date": "2021-03-17",
            "rates": {"RUB": 87.2}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        rate = get_exchange_rate("EUR")
        assert rate == 87.2

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_api_error(self, mock_get):
        """Тест: API возвращает ошибку — выбрасывается исключение."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"type": "invalid_access_key"}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Не удалось получить курс"):
            get_exchange_rate("USD")


class TestConvertToRubles:

    def test_convert_rub_transaction(self):
        """Тест: транзакция в рублях — конвертация не требуется."""
        transaction = {
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"code": "RUB", "name": "RUB"}
            }
        }
        result = convert_to_rubles(transaction)
        assert result == 1000.0
        assert isinstance(result, float)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_usd_transaction(self, mock_rate):
        """Тест: транзакция в USD — конвертация через API."""
        mock_rate.return_value = 73.5

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD", "name": "USD"}
            }
        }
        result = convert_to_rubles(transaction)
        assert result == 7350.0
        mock_rate.assert_called_once_with("USD")

    @patch("src.external_api.get_exchange_rate")
    def test_convert_eur_transaction(self, mock_rate):
        """Тест: транзакция в EUR — конвертация через API."""
        mock_rate.return_value = 87.2

        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR", "name": "EUR"}
            }
        }
        result = convert_to_rubles(transaction)
        assert result == 4360.0
        mock_rate.assert_called_once_with("EUR")

    def test_convert_unsupported_currency(self):
        """Тест: неподдерживаемая валюта — выбрасывается исключение."""
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "GBP", "name": "GBP"}
            }
        }
        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            convert_to_rubles(transaction)

    def test_convert_empty_transaction(self):
        """Тест: транзакция без данных — возвращается 0.0."""
        transaction = {}
        result = convert_to_rubles(transaction)
        assert result == 0.0

    @patch("src.external_api.get_exchange_rate")
    def test_convert_usd_rounding(self, mock_rate):
        """Тест: результат конвертации округляется до 2 знаков."""
        mock_rate.return_value = 73.456

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD", "name": "USD"}
            }
        }
        result = convert_to_rubles(transaction)
        assert result == 7345.60
