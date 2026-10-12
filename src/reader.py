import csv
from typing import List, Dict, Any
import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла с использованием библиотеки csv.

    :param file_path: Путь к CSV-файлу.
    :return: Список словарей с данными о транзакциях.
    """
    transactions: List[Dict[str, Any]] = []

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        # Указываем delimiter=';', так как файл разделен точками с запятой
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            # Пропускаем строки, где все значения пустые (например, ";;;;;;;;")
            if any(row.values()):
                # Преобразуем числовые поля из строк в int для корректности данных
                row_id = row.get('id')
                if isinstance(row_id, str) and row_id.isdigit():
                    row['id'] = int(row_id)

                row_amount = row.get('amount')
                if isinstance(row_amount, str) and row_amount.isdigit():
                    row['amount'] = int(row_amount)

                transactions.append(row)

    return transactions


def read_xlsx_transactions(file_path: str) -> pd.DataFrame:
    """
    Считывает финансовые операции из XLSX-файла с использованием библиотеки pandas.

    :param file_path: Путь к XLSX-файлу.
    :return: DataFrame с данными о транзакциях.
    """
    # Считываем Excel-файл (требуется установленная библиотека openpyxl)
    df: pd.DataFrame = pd.read_excel(file_path)

    # Удаляем полностью пустые строки, если они есть в Excel-файле
    df = df.dropna(how='all').reset_index(drop=True)

    return df
