import pytest
import pandas as pd
from typing import List, Dict, Any

from reader import read_csv_transactions, read_xlsx_transactions


def test_read_csv_transactions(tmp_path) -> None:
    """Тест считывания и парсинга CSV-файла."""
    # Создаем тестовый CSV-контент с пустой строкой
    csv_content = """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-01-01T00:00:00Z;100;USD;USD;Card1;Card2;Transfer
;;;;;;;;
2;CANCELED;2023-01-02T00:00:00Z;200;EUR;EUR;Card3;Card4;Transfer"""

    csv_file = tmp_path / "test_transactions.csv"
    csv_file.write_text(csv_content, encoding='utf-8')

    result: List[Dict[str, Any]] = read_csv_transactions(str(csv_file))

    # Проверяем, что пустая строка была пропущена
    assert len(result) == 2

    # Проверяем корректность типов и значений
    assert result[0]['id'] == 1
    assert isinstance(result[0]['id'], int)
    assert result[0]['amount'] == 100
    assert result[1]['state'] == 'CANCELED'


def test_read_xlsx_transactions(tmp_path) -> None:
    """Тест считывания XLSX-файла с помощью pandas."""
    # Создаем тестовый DataFrame и сохраняем его в Excel
    df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', 'CANCELED'],
        'date': ['2023-01-01T00:00:00Z', '2023-01-02T00:00:00Z'],
        'amount': [100, 200],
        'currency_name': ['USD', 'EUR'],
        'currency_code': ['USD', 'EUR'],
        'from': ['Card1', 'Card3'],
        'to': ['Card2', 'Card4'],
        'description': ['Transfer', 'Transfer']
    })

    excel_file = tmp_path / "test_transactions.xlsx"
    df.to_excel(str(excel_file), index=False)

    result_df: pd.DataFrame = read_xlsx_transactions(str(excel_file))

    # Проверяем количество строк и значения
    assert len(result_df) == 2
    assert result_df.iloc[0]['id'] == 1
    assert result_df.iloc[1]['state'] == 'CANCELED'
