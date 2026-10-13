from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import pandas as pd  # type: ignore[import-untyped]


@dataclass(frozen=True)
class Transaction:
    """Модель финансовой операции."""

    id: int
    state: str
    date: datetime
    amount: int
    currency_name: str
    currency_code: str
    from_account: str
    to_account: str
    description: str


COLUMNS: tuple[str, ...] = (
    "id",
    "state",
    "date",
    "amount",
    "currency_name",
    "currency_code",
    "from",
    "to",
    "description",
)


def _parse_row(row: Sequence[str]) -> Transaction | None:
    """Преобразует список строк в объект Transaction.

    Возвращает None, если строка пустая или некорректная.
    """
    if len(row) < len(COLUMNS):
        return None

    raw_id, raw_state, raw_date, raw_amount, \
        currency_name, currency_code, from_account, to_account, description = row[:9]

    # Пропускаем полностью пустые строки
    if not raw_id.strip():
        return None

    try:
        transaction_id = int(raw_id)
        amount = int(raw_amount)
        date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None

    return Transaction(
        id=transaction_id,
        state=raw_state,
        date=date,
        amount=amount,
        currency_name=currency_name,
        currency_code=currency_code,
        from_account=from_account,
        to_account=to_account,
        description=description,
    )


def read_transactions_csv(
    file_path: str | Path,
    delimiter: str = ";",
    encoding: str = "utf-8",
) -> list[Transaction]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: путь к CSV-файлу.
        delimiter: разделитель колонок (по умолчанию ';').
        encoding: кодировка файла.

    Returns:
        Список объектов Transaction.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если файл пуст или отсутствуют обязательные колонки.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    transactions: list[Transaction] = []

    with path.open("r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)

        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV-файл пуст: {path}") from exc

        missing = [col for col in COLUMNS if col not in header]
        if missing:
            raise ValueError(
                f"В CSV-файле отсутствуют колонки: {', '.join(missing)}"
            )

        # Приводим заголовок к ожидаемому порядку колонок
        index_map = {name: header.index(name) for name in COLUMNS}

        for row in reader:
            if len(row) < len(header):
                continue
            ordered = [row[index_map[name]] for name in COLUMNS]
            transaction = _parse_row(ordered)
            if transaction is not None:
                transactions.append(transaction)

    return transactions


def read_transactions_xlsx(
    file_path: str | Path,
    sheet_name: str | int = 0,
) -> list[Transaction]:
    """Считывает финансовые операции из XLSX-файла.

    Args:
        file_path: путь к XLSX-файлу.
        sheet_name: имя листа или его индекс.

    Returns:
        Список объектов Transaction.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если отсутствуют обязательные колонки.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    df: pd.DataFrame = pd.read_excel(
        path, sheet_name=sheet_name, dtype=str, engine="openpyxl"
    )

    missing = [col for col in COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"В XLSX-файле отсутствуют колонки: {', '.join(missing)}"
        )

    transactions: list[Transaction] = []
    for _, row in df.iterrows():
        values: list[str] = [str(row[col]) if pd.notna(row[col]) else ""
                            for col in COLUMNS]
        transaction = _parse_row(values)
        if transaction is not None:
            transactions.append(transaction)

    return transactions


def transactions_to_dicts(
    transactions: Iterable[Transaction],
) -> list[dict[str, Any]]:
    """Преобразует список Transaction в список словарей.

    Полезно для сериализации или дальнейшей обработки.
    """
    result: list[dict[str, Any]] = []
    for t in transactions:
        result.append(
            {
                "id": t.id,
                "state": t.state,
                "date": t.date.isoformat(),
                "amount": t.amount,
                "currency_name": t.currency_name,
                "currency_code": t.currency_code,
                "from": t.from_account,
                "to": t.to_account,
                "description": t.description,
            }
        )
    return result


def iter_transactions_csv(
    file_path: str | Path,
    delimiter: str = ";",
    encoding: str = "utf-8",
) -> Iterator[Transaction]:
    """Ленивый генератор транзакций из CSV-файла.

    Позволяет обрабатывать большие файлы без загрузки всего в память.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with path.open("r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV-файл пуст: {path}") from exc

        missing = [col for col in COLUMNS if col not in header]
        if missing:
            raise ValueError(
                f"В CSV-файле отсутствуют колонки: {', '.join(missing)}"
            )

        index_map = {name: header.index(name) for name in COLUMNS}

        for row in reader:
            if len(row) < len(header):
                continue
            ordered = [row[index_map[name]] for name in COLUMNS]
            transaction = _parse_row(ordered)
            if transaction is not None:
                yield transaction


if __name__ == "__main__":
    csv_transactions = read_transactions_csv("transactions.csv")
    xlsx_transactions = read_transactions_xlsx("transactions_excel.xlsx")

    print(f"Из CSV: {len(csv_transactions)} транзакций")
    print(f"Из XLSX: {len(xlsx_transactions)} транзакций")
    print(f"Первая транзакция из CSV: {csv_transactions[0]}")
