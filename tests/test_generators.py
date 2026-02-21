"""
Тесты для модуля generators.
"""

from typing import Any
from typing import Dict
from typing import List

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


# Тесты для filter_by_currency
class TestFilterByCurrency:
    """Тесты функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions):
        """Проверка фильтрации по USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2
        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub_transactions(self, sample_transactions):
        """Проверка фильтрации по RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_nonexistent_currency(self, sample_transactions):
        """Проверка фильтрации по несуществующей валюте."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_empty_transactions_list(self, empty_transactions):
        """Проверка с пустым списком транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert len(result) == 0

    @pytest.mark.parametrize("currency,expected_count", [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0)
    ])
    def test_filter_by_currency_parametrized(self, sample_transactions, currency, expected_count):
        """Параметризованный тест фильтрации."""
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == expected_count

    def test_iterator_behavior(self, sample_transactions):
        """Проверка поведения итератора."""
        usd_iterator = filter_by_currency(sample_transactions, "USD")

        # Получаем первую транзакцию
        first = next(usd_iterator)
        assert first["id"] == 939719570

        # Получаем вторую транзакцию
        second = next(usd_iterator)
        assert second["id"] == 142264268

        # Проверяем, что больше нет транзакций
        with pytest.raises(StopIteration):
            next(usd_iterator)


# Тесты для transaction_descriptions
class TestTransactionDescriptions:
    """Тесты функции transaction_descriptions."""

    def test_get_descriptions(self, sample_transactions):
        """Проверка получения описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]
        assert descriptions == expected

    def test_empty_transactions(self, empty_transactions):
        """Проверка с пустым списком."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert len(descriptions) == 0

    def test_generator_behavior(self, sample_transactions):
        """Проверка поведения генератора."""
        desc_gen = transaction_descriptions(sample_transactions)

        assert next(desc_gen) == "Перевод организации"
        assert next(desc_gen) == "Перевод со счета на счет"
        assert next(desc_gen) == "Перевод со счета на счет"

        with pytest.raises(StopIteration):
            next(desc_gen)

    @pytest.mark.parametrize("index,expected", [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (2, "Перевод со счета на счет")
    ])
    def test_specific_descriptions(self, sample_transactions, index, expected):
        """Параметризованная проверка конкретных описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert descriptions[index] == expected


# Тесты для card_number_generator
class TestCardNumberGenerator:
    """Тесты генератора card_number_generator."""

    def test_generate_small_range(self):
        """Проверка генерации в небольшом диапазоне."""
        cards = list(card_number_generator(1, 5))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]
        assert cards == expected

    def test_format_with_leading_zeros(self):
        """Проверка форматирования с ведущими нулями."""
        card = next(card_number_generator(1, 1))
        assert card == "0000 0000 0000 0001"

        card = next(card_number_generator(999, 999))
        assert card == "0000 0000 0000 0999"

    def test_single_number(self):
        """Проверка генерации одного номера."""
        card = next(card_number_generator(1234567890123456, 1234567890123456))
        assert card == "1234 5678 9012 3456"

    def test_max_value(self):
        """Проверка максимального значения."""
        card = next(card_number_generator(9999999999999999, 9999999999999999))
        assert card == "9999 9999 9999 9999"

    def test_range_length(self):
        """Проверка длины сгенерированного диапазона."""
        cards = list(card_number_generator(10, 20))
        assert len(cards) == 11  # 20 - 10 + 1 = 11

    @pytest.mark.parametrize("start,stop,expected_count", [
        (1, 1, 1),
        (1, 10, 10),
        (100, 200, 101),
        (9999999999999990, 9999999999999999, 10)
    ])
    def test_range_counts(self, start, stop, expected_count):
        """Параметризованная проверка количества генерируемых номеров."""
        cards = list(card_number_generator(start, stop))
        assert len(cards) == expected_count

    def test_invalid_start_value(self):
        """Проверка обработки недопустимого начального значения."""
        with pytest.raises(ValueError, match="Номер карты должен быть в диапазоне от 1 до 9999999999999999"):
            next(card_number_generator(0, 10))

    def test_invalid_stop_value(self):
        """Проверка обработки недопустимого конечного значения."""
        with pytest.raises(ValueError, match="Номер карты должен быть в диапазоне от 1 до 9999999999999999"):
            next(card_number_generator(1, 10000000000000000))

    def test_generator_exhaustion(self):
        """Проверка истощения генератора."""
        gen = card_number_generator(1, 3)
        assert next(gen) == "0000 0000 0000 0001"
        assert next(gen) == "0000 0000 0000 0002"
        assert next(gen) == "0000 0000 0000 0003"

        with pytest.raises(StopIteration):
            next(gen)
