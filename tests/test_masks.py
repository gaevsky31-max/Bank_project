"""Тест для модуля masks.py"""

import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


# ========== ТЕСТЫ С ПАРАМЕТРИЗАЦИЕЙ ==========
@pytest.mark.parametrize("card_number, expected", [
    (7000792289606361, "7000 79** **** 6361"),
    (7158300734726758, "7158 30** **** 6758"),
    (6831982476737658, "6831 98** **** 7658"),
    (1234567890123456, "1234 56** **** 3456"),
])
def test_get_mask_card_number_valid(card_number, expected):
    """Параметризованный тест валидных номеров карт."""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize("invalid_card", [
    12345,           # 5 цифр
    123456789012345,  # 15 цифр
    12345678901234567,  # 17 цифр
    0,               # 1 цифра
])
def test_get_mask_card_number_invalid(invalid_card):
    """Параметризованный тест невалидных номеров карт."""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize("account_number, expected", [
    (73654108430135874305, "**4305"),
    (64686473678894779589, "**9589"),
    (35383033474447895560, "**5560"),
    (1234567890, "**7890"),
])
def test_get_mask_account_valid(account_number, expected):
    """Параметризованный тест валидных номеров счетов."""
    result = get_mask_account(account_number)
    assert result == expected


@pytest.mark.parametrize("invalid_account", [
    123,    # 3 цифры
    12,     # 2 цифры
    1,      # 1 цифра
    0,      # 0 (1 цифра)
])
def test_get_mask_account_invalid(invalid_account):
    """Параметризованный тест невалидных номеров счетов."""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)


# ========== ТЕСТЫ С ИСПОЛЬЗОВАНИЕМ ФИКСТУР ==========
def test_get_mask_card_number_with_fixture(valid_card_numbers):
    """Тест с использованием фикстуры valid_card_numbers."""
    for card in valid_card_numbers:
        result = get_mask_card_number(card)
        assert isinstance(result, str)
        assert len(result) == 19  # XXXX XX** **** XXXX
        assert "**" in result


def test_get_mask_account_with_fixture(valid_account_numbers):
    """Тест с использованием фикстуры valid_account_numbers."""
    for account in valid_account_numbers:
        result = get_mask_account(account)
        assert isinstance(result, str)
        assert result.startswith("**")
        assert len(result) == 6  # **XXXX


# ========== ВАШИ ОРИГИНАЛЬНЫЕ ТЕСТЫ ==========
def test_get_mask_card_number_original():
    """Оригинальный тест для проверки маскировки номера карты."""
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    assert get_mask_card_number(1234567892101112) == "1234 56** **** 1112"


def test_get_mask_card_invalid_original():
    """Оригинальный тест: если введен некорректный номер карты."""
    with pytest.raises(ValueError):
        get_mask_card_number(12345)


def test_get_mask_account_original():
    """Оригинальный тест для проверки маскировки номера счета."""
    assert get_mask_account(73654108430135874305) == "**4305"
    assert get_mask_account(1234567890) == "**7890"


def test_get_mask_account_invalid_original():
    """Оригинальный тест: если введен некорректный номер счета."""
    with pytest.raises(ValueError):
        get_mask_account(123)
