"""Тесты для модуля processing.py"""

import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date


# ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ filter_by_state ==========
class TestFilterByState:
    """Тесты для функции filter_by_state с параметризацией."""

    @pytest.fixture
    def test_operations(self):
        """Фикстура с тестовыми операциями."""
        return [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 123456789, "state": "EXECUTED", "date": "2020-01-01T00:00:00.000000"},
        ]

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 3),
        ("CANCELED", 2),
        ("PENDING", 0),
    ])
    def test_filter_by_state_parametrized(self, test_operations, state, expected_count):
        """Параметризованный тест фильтрации."""
        result = filter_by_state(test_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            for operation in result:
                assert operation["state"] == state

    def test_filter_by_state_default(self, test_operations):
        """Тест фильтрации со статусом по умолчанию."""
        result = filter_by_state(test_operations)
        assert len(result) == 3
        for operation in result:
            assert operation["state"] == "EXECUTED"

    def test_filter_by_state_with_fixture(self, sample_transactions):
        """Тест с использованием фикстуры."""
        executed = filter_by_state(sample_transactions, "EXECUTED")
        assert len(executed) == 3

        canceled = filter_by_state(sample_transactions, "CANCELED")
        assert len(canceled) == 2

        for op in executed:
            assert op["state"] == "EXECUTED"
        for op in canceled:
            assert op["state"] == "CANCELED"

    def test_filter_by_state_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    def test_filter_by_state_no_state_field(self, transactions_without_state):
        """Тест фильтрации транзакций без поля state."""
        result = filter_by_state(transactions_without_state, "EXECUTED")
        assert len(result) == 0

    def test_filter_by_state_single_transaction(self, single_transaction):
        """Тест фильтрации с одной транзакцией."""
        result = filter_by_state(single_transaction, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 1


# ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ sort_by_date ==========
class TestSortByDate:
    """Тесты для функции sort_by_date с параметризацией."""

    @pytest.fixture
    def test_operations(self):
        """Фикстура с тестовыми операциями."""
        return [
            {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 5, "state": "EXECUTED", "date": "2020-01-01T00:00:00.000000"},
        ]

    @pytest.mark.parametrize("reverse, expected_first_id", [
        (True, 5),
        (False, 2),
    ])
    def test_sort_by_date_parametrized(self, test_operations, reverse, expected_first_id):
        """Параметризованный тест сортировки."""
        result = sort_by_date(test_operations, reverse)
        assert len(result) == 5
        assert result[0]["id"] == expected_first_id

        dates = [op["date"] for op in result]
        sorted_dates = sorted(dates, reverse=reverse)
        assert dates == sorted_dates

    def test_sort_by_date_default(self, test_operations):
        """Тест сортировки по умолчанию."""
        result = sort_by_date(test_operations)
        assert result[0]["id"] == 5
        assert result[-1]["id"] == 2

    def test_sort_by_date_with_fixture(self, unsorted_transactions):
        """Тест с использованием фикстуры."""
        result_desc = sort_by_date(unsorted_transactions, True)
        dates_desc = [op["date"] for op in result_desc]
        assert dates_desc == sorted(dates_desc, reverse=True)

        result_asc = sort_by_date(unsorted_transactions, False)
        dates_asc = [op["date"] for op in result_asc]
        assert dates_asc == sorted(dates_asc, reverse=False)

    def test_sort_by_date_empty_list(self):
        """Тест сортировки пустого списка."""
        result = sort_by_date([], True)
        assert result == []

    def test_sort_by_date_single_transaction(self, single_transaction):
        """Тест сортировки с одной транзакцией."""
        result = sort_by_date(single_transaction, True)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_by_date_same_dates(self):
        """Тест сортировки с одинаковыми датами."""
        operations = [
            {"id": 1, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"},
            {"id": 2, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"},
            {"id": 3, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"},
        ]
        result = sort_by_date(operations, True)
        assert [op["id"] for op in result] == [1, 2, 3]

    def test_sort_by_date_missing_date_field(self):
        """Тест сортировки без поля date."""
        operations = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"},
        ]
        result = sort_by_date(operations, True)
        assert len(result) == 2


# ========== ОРИГИНАЛЬНЫЕ ТЕСТЫ ==========
def test_filter_by_state_original():
    """Оригинальный тест для filter_by_state."""
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    result_default = filter_by_state(test_data)
    assert len(result_default) == 2
    for operation in result_default:
        assert operation["state"] == "EXECUTED"

    result_canceled = filter_by_state(test_data, state="CANCELED")
    assert len(result_canceled) == 2
    for operation in result_canceled:
        assert operation["state"] == "CANCELED"


def test_sort_by_date_original():
    """Оригинальный тест для sort_by_date."""
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    result_desc = sort_by_date(test_data)
    assert len(result_desc) == 4
    assert result_desc[0]["date"] == "2019-07-03T18:35:29.512364"
    assert result_desc[1]["date"] == "2018-10-14T08:21:33.419441"
    assert result_desc[2]["date"] == "2018-09-12T21:27:25.241689"
    assert result_desc[3]["date"] == "2018-06-30T02:08:58.425572"

    result_asc = sort_by_date(test_data, False)
    assert len(result_asc) == 4
    assert result_asc[0]["date"] == "2018-06-30T02:08:58.425572"
    assert result_asc[1]["date"] == "2018-09-12T21:27:25.241689"
    assert result_asc[2]["date"] == "2018-10-14T08:21:33.419441"
    assert result_asc[3]["date"] == "2019-07-03T18:35:29.512364"
