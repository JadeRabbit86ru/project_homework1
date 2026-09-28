import json
import os
import tempfile

from src.utils import load_transactions_from_json


class TestLoadTransactionsFromJson:

    def test_load_valid_json(self):
        """Тест загрузки валидного JSON-файла со списком транзакций."""
        transactions = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200}
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(transactions, f)
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == transactions
            assert len(result) == 2
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        """Тест: файл не найден — возвращается пустой список."""
        result = load_transactions_from_json("/nonexistent/path/operations.json")
        assert result == []

    def test_empty_file(self):
        """Тест: пустой файл — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_file_contains_dict_not_list(self):
        """Тест: файл содержит словарь, а не список — возвращается пустой список."""
        data = {"id": 1, "amount": 100}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_file_contains_string_not_list(self):
        """Тест: файл содержит строку, а не список — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump("not a list", f)
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_invalid_json(self):
        """Тест: невалидный JSON — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("{invalid json content}")
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_empty_list(self):
        """Тест: файл содержит пустой список — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([], f)
            temp_path = f.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)
