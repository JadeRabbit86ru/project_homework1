from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
import pytest

from reader import COLUMNS
from reader import Transaction
from reader import iter_transactions_csv
from reader import read_transactions_csv
from reader import read_transactions_xlsx
from reader import transactions_to_dicts

# ---------- Фикстуры ----------


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Создаёт временный CSV-файл с тестовыми данными."""
    file_path = tmp_path / "sample.csv"
    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(COLUMNS)
        writer.writerow(
            [
                "650703",
                "EXECUTED",
                "2023-09-05T11:30:32Z",
                "16210",
                "Sol",
                "PEN",
                "Счет 58803664561298323391",
                "Счет 39745660563456619397",
                "Перевод организации",
            ]
        )
        writer.writerow(
            [
                "3598919",
                "EXECUTED",
                "2020-12-06T23:00:58Z",
                "29740",
                "Peso",
                "COP",
                "Discover 3172601889670065",
                "Discover 0720428384694643",
                "Перевод с карты на карту",
            ]
        )
    return file_path


@pytest.fixture
def sample_csv_with_empty(tmp_path: Path) -> Path:
    """CSV-файл с пустой строкой и невалидной записью."""
    file_path = tmp_path / "sample_empty.csv"
    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(COLUMNS)
        writer.writerow([""] * 9)
        writer.writerow(
            [
                "632926",
                "PENDING",
                "2021-11-27T00:46:09Z",
                "29553",
                "Yuan Renminbi",
                "CNY",
                "American Express 6477627838877562",
                "Счет 88381741644903346269",
                "Перевод организации",
            ]
        )
        writer.writerow(
            [
                "bad_id",
                "PENDING",
                "bad_date",
                "29553",
                "Yuan Renminbi",
                "CNY",
                "a",
                "b",
                "c",
            ]
        )
    return file_path


@pytest.fixture
def sample_xlsx(tmp_path: Path) -> Path:
    """Создаёт временный XLSX-файл с тестовыми данными."""
    file_path = tmp_path / "sample.xlsx"
    df = pd.DataFrame(
        [
            [
                "650703",
                "EXECUTED",
                "2023-09-05T11:30:32Z",
                "16210",
                "Sol",
                "PEN",
                "Счет 58803664561298323391",
                "Счет 39745660563456619397",
                "Перевод организации",
            ],
            [
                "3598919",
                "EXECUTED",
                "2020-12-06T23:00:58Z",
                "29740",
                "Peso",
                "COP",
                "Discover 3172601889670065",
                "Discover 0720428384694643",
                "Перевод с карты на карту",
            ],
        ],
        columns=list(COLUMNS),
    )
    df.to_excel(file_path, index=False, engine="openpyxl")
    return file_path


# ---------- Тесты read_transactions_csv ----------


class TestReadTransactionsCsv:
    def test_reads_all_rows(self, sample_csv: Path) -> None:
        result = read_transactions_csv(sample_csv)
        assert len(result) == 2

    def test_returns_transaction_objects(self, sample_csv: Path) -> None:
        result = read_transactions_csv(sample_csv)
        assert all(isinstance(t, Transaction) for t in result)

    def test_parses_fields(self, sample_csv: Path) -> None:
        t = read_transactions_csv(sample_csv)[0]
        assert t.id == 650703
        assert t.state == "EXECUTED"
        assert t.date == datetime(2023, 9, 5, 11, 30, 32)
        assert t.amount == 16210
        assert t.currency_name == "Sol"
        assert t.currency_code == "PEN"
        assert t.from_account == "Счет 58803664561298323391"
        assert t.to_account == "Счет 39745660563456619397"
        assert t.description == "Перевод организации"

    def test_skips_empty_and_invalid_rows(self, sample_csv_with_empty: Path) -> None:
        result = read_transactions_csv(sample_csv_with_empty)
        assert len(result) == 1
        assert result[0].id == 632926

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            read_transactions_csv(tmp_path / "missing.csv")

    def test_empty_file_raises(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty.csv"
        empty.write_text("", encoding="utf-8")
        with pytest.raises(ValueError, match="пуст"):
            read_transactions_csv(empty)

    def test_missing_columns_raise(self, tmp_path: Path) -> None:
        file_path = tmp_path / "bad.csv"
        with file_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["id", "state", "date"])
            writer.writerow(["1", "EXECUTED", "2023-01-01T00:00:00Z"])
        with pytest.raises(ValueError, match="отсутствуют колонки"):
            read_transactions_csv(file_path)


# ---------- Тесты read_transactions_xlsx ----------


class TestReadTransactionsXlsx:
    def test_reads_all_rows(self, sample_xlsx: Path) -> None:
        result = read_transactions_xlsx(sample_xlsx)
        assert len(result) == 2

    def test_parses_fields(self, sample_xlsx: Path) -> None:
        t = read_transactions_xlsx(sample_xlsx)[0]
        assert t.id == 650703
        assert t.amount == 16210
        assert t.currency_code == "PEN"

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            read_transactions_xlsx(tmp_path / "missing.xlsx")

    def test_missing_columns_raise(self, tmp_path: Path) -> None:
        file_path = tmp_path / "bad.xlsx"
        pd.DataFrame({"id": [1], "state": ["EXECUTED"]}).to_excel(file_path, index=False, engine="openpyxl")
        with pytest.raises(ValueError, match="отсутствуют колонки"):
            read_transactions_xlsx(file_path)


# ---------- Тесты iter_transactions_csv ----------


class TestIterTransactionsCsv:
    def test_yields_transactions(self, sample_csv: Path) -> None:
        result = list(iter_transactions_csv(sample_csv))
        assert len(result) == 2

    def test_is_lazy(self, sample_csv: Path) -> None:
        generator = iter_transactions_csv(sample_csv)
        first = next(generator)
        assert isinstance(first, Transaction)

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            list(iter_transactions_csv(tmp_path / "missing.csv"))


# ---------- Тесты transactions_to_dicts ----------


class TestTransactionsToDicts:
    def test_converts_to_dicts(self, sample_csv: Path) -> None:
        transactions = read_transactions_csv(sample_csv)
        dicts = transactions_to_dicts(transactions)
        assert len(dicts) == 2
        assert dicts[0]["id"] == 650703
        assert dicts[0]["date"] == "2023-09-05T11:30:32"
        assert dicts[0]["from"] == "Счет 58803664561298323391"

    def test_empty_input(self) -> None:
        assert transactions_to_dicts([]) == []


# ---------- Сравнение CSV и XLSX ----------


class TestCsvXlsxParity:
    def test_same_content(self, sample_csv: Path, sample_xlsx: Path) -> None:
        csv_result = read_transactions_csv(sample_csv)
        xlsx_result = read_transactions_xlsx(sample_xlsx)
        assert csv_result == xlsx_result
