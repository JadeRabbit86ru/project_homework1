import csv
from typing import Any
from typing import Dict
from typing import List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    :param file_path: Путь к CSV-файлу.
    :return: Список словарей с данными о транзакциях.
    """
    transactions: List[Dict[str, Any]] = []

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            # Пропускаем полностью пустые строки
            if not any(row.values()):
                continue

            # Преобразуем числовые поля в int, если они представлены как строки цифр
            if 'id' in row and isinstance(row['id'], str) and row['id'].isdigit():
                row['id'] = int(row['id'])
            if 'amount' in row and isinstance(row['amount'], str) and row['amount'].isdigit():
                row['amount'] = int(row['amount'])

            transactions.append(row)

    return transactions


def read_xlsx_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    :param file_path: Путь к XLSX-файлу.
    :return: Список словарей с данными о транзакциях.
    """
    # Читаем Excel и удаляем полностью пустые строки
    df = pd.read_excel(file_path)
    df = df.dropna(how='all')

    # Заменяем NaN на None для корректного преобразования в словари Python
    df = df.where(pd.notnull(df), None)

    # Преобразуем DataFrame в список словарей
    transactions = df.to_dict(orient='records')

    # Приводим числовые поля к int, если они являются целыми числами
    # (pandas часто делает их float из-за наличия пустых ячеек в столбце)
    for row in transactions:
        if isinstance(row.get('id'), float) and float(row['id']).is_integer():
            row['id'] = int(row['id'])
        if isinstance(row.get('amount'), float) and float(row['amount']).is_integer():
            row['amount'] = int(row['amount'])

    return transactions