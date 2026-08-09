import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура с примерами транзакций для тестирования."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-15T10:30:00.000000",
            "amount": 1000,
        },
        {
            "id": 2,
            "state": "PENDING",
            "date": "2024-01-14T09:00:00.000000",
            "amount": 2000,
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-16T15:45:00.000000",
            "amount": 3000,
        },
        {
            "id": 4,
            "state": "CANCELED",
            "date": "2024-01-13T08:00:00.000000",
            "amount": 4000,
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2024-01-15T10:30:00.000000",
            "amount": 5000,
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций."""
    return []


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_executed(self, sample_transactions):
        """Тестирование фильтрации по статусу EXECUTED."""
        result = filter_by_state(sample_transactions, "EXECUTED")
        assert len(result) == 3
        for item in result:
            assert item["state"] == "EXECUTED"

    def test_filter_pending(self, sample_transactions):
        """Тестирование фильтрации по статусу PENDING."""
        result = filter_by_state(sample_transactions, "PENDING")
        assert len(result) == 1
        assert result[0]["state"] == "PENDING"

    def test_filter_canceled(self, sample_transactions):
        """Тестирование фильтрации по статусу CANCELED."""
        result = filter_by_state(sample_transactions, "CANCELED")
        assert len(result) == 1
        assert result[0]["state"] == "CANCELED"

    def test_filter_nonexistent_state(self, sample_transactions):
        """Проверка работы функции при отсутствии словарей с указанным статусом."""
        result = filter_by_state(sample_transactions, "NONEXISTENT")
        assert len(result) == 0
        assert result == []

    def test_filter_empty_list(self, empty_transactions):
        """Проверка работы функции с пустым списком."""
        result = filter_by_state(empty_transactions, "EXECUTED")
        assert result == []

    @pytest.mark.parametrize(
        "state,expected_count",
        [
            ("EXECUTED", 3),
            ("PENDING", 1),
            ("CANCELED", 1),
            ("NONEXISTENT", 0),
        ],
    )
    def test_parametrized_states(self, sample_transactions, state, expected_count):
        """Параметризация тестов для различных возможных значений статуса state."""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count

    def test_default_state(self, sample_transactions):
        """Проверка значения state по умолчанию (EXECUTED)."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 3
        for item in result:
            assert item["state"] == "EXECUTED"


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_descending(self, sample_transactions):
        """Тестирование сортировки по убыванию (по умолчанию)."""
        result = sort_by_date(sample_transactions)
        # Проверяем что даты отсортированы в порядке убывания
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self, sample_transactions):
        """Тестирование сортировки по возрастанию."""
        result = sort_by_date(sample_transactions, reverse=False)
        # Проверяем что даты отсортированы в порядке возрастания
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_sort_same_dates(self):
        """Проверка корректности сортировки при одинаковых датах."""
        transactions = [
            {"id": 1, "date": "2024-01-15T10:30:00.000000", "amount": 1000},
            {"id": 2, "date": "2024-01-15T10:30:00.000000", "amount": 2000},
            {"id": 3, "date": "2024-01-15T10:30:00.000000", "amount": 3000},
        ]
        result = sort_by_date(transactions)
        assert len(result) == 3
        # Все элементы должны остаться в списке
        ids = [item["id"] for item in result]
        assert set(ids) == {1, 2, 3}

    def test_sort_empty_list(self, empty_transactions):
        """Проверка работы функции с пустым списком."""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_sort_single_item(self):
        """Проверка сортировки списка с одним элементом."""
        transactions = [{"id": 1, "date": "2024-01-15T10:30:00.000000"}]
        result = sort_by_date(transactions)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_missing_date_key(self):
        """Тесты на работу функции с элементами без ключа date."""
        transactions = [
            {"id": 1, "date": "2024-01-15T10:30:00.000000"},
            {"id": 2},  # Нет ключа date
            {"id": 3, "date": "2024-01-14T10:30:00.000000"},
        ]
        result = sort_by_date(transactions)
        # Элемент без даты должен быть отсортирован как "" (пустая строка)
        assert len(result) == 3
        # Пустая строка должна быть в конце при сортировке по убыванию
        ids = [item["id"] for item in result]
        assert ids[0] == 1  # Самая поздняя дата
        assert ids[-1] == 2  # Элемент без даты

    def test_sort_invalid_date_format(self):
        """Тесты на работу функции с некорректными форматами дат."""
        transactions = [
            {"id": 1, "date": "2024-01-15T10:30:00.000000"},
            {"id": 2, "date": "invalid_date"},
            {"id": 3, "date": "2024-01-14T10:30:00.000000"},
        ]
        result = sort_by_date(transactions)
        # Функция должна работать, сортируя строки лексикографически
        assert len(result) == 3

    @pytest.mark.parametrize(
        "reverse,expected_first_date",
        [
            (True, "2024-01-16T15:45:00.000000"),  # По убыванию - самая поздняя
            (False, "2024-01-13T08:00:00.000000"),  # По возрастанию - самая ранняя
        ],
    )
    def test_parametrized_sort_order(
        self, sample_transactions, reverse, expected_first_date
    ):
        """Параметризованный тест для проверки порядка сортировки."""
        result = sort_by_date(sample_transactions, reverse=reverse)
        assert result[0]["date"] == expected_first_date
