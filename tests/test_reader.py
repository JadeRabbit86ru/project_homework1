from typing import Any
from typing import Dict
from typing import List

import pandas as pd
import pytest

from reader import read_csv_transactions
from reader import read_xlsx_transactions


def test_read_csv_transactions(tmp_path) -> None:
    """Тест считывания и парсинга CSV-файла."""
    csv_content = """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-01-01T00:00:00Z;100;USD;USD;Card1;Card2;Transfer
;;;;;;;;"""

    csv_file = tmp_path / "test_transactions.csv"
    csv_file.write_text(csv_content, encoding='utf-8')

    result = read_csv_transactions(str(csv_file))

    assert len(result) == 1
    assert result[0]['id'] == 1
    assert isinstance(result[0]['id'], int)
    assert result[0]['amount'] == 100


def test_read_xlsx_transactions(tmp_path) -> None:
    """Тест считывания XLSX-файла и проверки возврата списка словарей."""
    # Создаем тестовый DataFrame с одной пустой ячейкой (None)
    df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', 'CANCELED'],
        'date': ['2023-01-01T00:00:00Z', '2023-01-02T00:00:00Z'],
        'amount': [100, 200],
        'currency_name': ['USD', 'EUR'],
        'currency_code': ['USD', 'EUR'],
        'from': ['Card1', None],
        'to': ['Card2', 'Card4'],
        'description': ['Transfer', 'Transfer']
    })

    excel_file = tmp_path / "test_transactions.xlsx"
    df.to_excel(str(excel_file), index=False)

    result = read_xlsx_transactions(str(excel_file))

    # Проверяем, что вернулся именно список словарей
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)

    # Проверяем значения и типы
    assert result[0]['id'] == 1
    assert isinstance(result[0]['id'], int)
    assert result[1]['state'] == 'CANCELED'
    # Проверяем, что пустое значение корректно стало None, а не NaN
    assert result[1]['from'] is None
