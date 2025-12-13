"""Тесты для модуля widget.py"""

import pytest

from src.widget import get_date
from src.widget import mask_account_card


# ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ mask_account_card ==========
class TestMaskAccountCard:
    """Тесты для функции mask_account_card с параметризацией."""

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            # Тесты для карт
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            # Тесты для счетов
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 64686473678894779589", "Счет **9589"),
            ("Счет 35383033474447895560", "Счет **5560"),
        ],
    )
    def test_mask_account_card_valid(self, input_str, expected):
        """Параметризованный тест валидных строк с картами/счетами."""
        result = mask_account_card(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",  # пустая строка
            "   ",  # только пробелы
            "Карта",  # нет номера
            "Счет 123",  # слишком короткий номер
            "Visa Platinum abc123",  # не цифры в номере
            "1234567890123456",  # только цифры, без типа
        ],
    )
    def test_mask_account_card_invalid(self, invalid_input):
        """Параметризованный тест невалидных строк."""
        result = mask_account_card(invalid_input)
        # Функция должна вернуть исходную строку при ошибке
        assert result == invalid_input

    def test_mask_account_card_with_fixture(self, transaction_strings):
        """Тест с использованием фикстуры transaction_strings."""
        for trans_str in transaction_strings:
            result = mask_account_card(trans_str)
            assert isinstance(result, str)
            # Проверяем что результат не пустой
            assert len(result) > 0
            # Если это карта - проверяем формат
            if "Счет" not in trans_str:
                assert "**" in result
                assert "****" in result


# ========== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ДЛЯ get_date ==========
class TestGetDate:
    """Тесты для функции get_date с параметризацией."""

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2023-12-31T23:59:59.999999", "31.12.2023"),
            ("2024-01-01T00:00:00.000000", "01.01.2024"),
            ("2019-08-26T10:50:58.294041", "26.08.2019"),
            ("2020-03-23T11:45:00.000000", "23.03.2020"),
            ("2021-12-01T00:00:00.000000", "01.12.2021"),
            ("2022-06-15T12:30:45.123456", "15.06.2022"),
        ],
    )
    def test_get_date_valid(self, input_date, expected):
        """Параметризованный тест валидных дат."""
        result = get_date(input_date)
        assert result == expected
        # Проверяем формат: DD.MM.YYYY
        assert len(result) == 10  # DD.MM.YYYY
        assert result[2] == "."
        assert result[5] == "."

    @pytest.mark.parametrize(
        "invalid_date, expected",
        [
            ("", ""),  # пустая строка - функция возвращает как есть
            ("11.03.2024", "11.03.2024"),  # уже в нужном формате
            ("invalid-date", "invalid-date"),  # невалидная дата
            ("2024/03/11T02:26:18.671407", "2024/03/11T02:26:18.671407"),
        ],
    )
    def test_get_date_invalid(self, invalid_date, expected):
        """Параметризованный тест невалидных дат."""
        result = get_date(invalid_date)
        assert result == expected

    def test_get_date_with_fixture(self, date_strings):
        """Тест с использованием фикстуры date_strings."""
        for date_str in date_strings:
            result = get_date(date_str)
            assert isinstance(result, str)
            # Проверяем что дата в правильном формате
            parts = result.split(".")
            assert len(parts) == 3
            day, month, year = parts
            assert len(day) == 2
            assert len(month) == 2
            assert len(year) == 4


# ========== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ==========
def test_integration_with_masks():
    """Тест интеграции widget с masks модулем."""
    test_cases = [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]

    for input_str, expected in test_cases:
        result = mask_account_card(input_str)
        assert result == expected


# ========== ОРИГИНАЛЬНЫЕ ТЕСТЫ (сохраняем) ==========
def test_mask_account_card_original():
    """Оригинальный тест для mask_account_card."""
    # Тест для карт
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"
    # Тест для счетов
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"
    assert mask_account_card("Счет 35383033474447895560") == "Счет **5560"


def test_get_date_original():
    """Оригинальный тест для get_date."""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-12-31T23:59:59.999999") == "31.12.2023"
    assert get_date("2024-01-01T00:00:00.000000") == "01.01.2024"
