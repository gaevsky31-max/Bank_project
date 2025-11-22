""" Тест для модуля masks.py"""

import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тест для проверки маскировки номера карты"""


# Проверяем, что функция возвращает правильный результат
assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
assert get_mask_card_number(1234567892101112) == "1234 56** **** 1112"


def test_get_mask_card_invalid() -> None:
    """Тест: если введен некорректный номер карты"""
    # Проверяем, что функция выведет ошибку при некорректном вводе номера карты
    with pytest.raises(ValueError):
        get_mask_card_number(12345)  # Формат не соответсвует 16-значному номеру карты


def test_get_mask_account() -> None:
    """Тест для проверки маскировки номера счета"""


# Проверяем, что функция возвращает правильный результат
assert get_mask_account(73654108430135874305) == "**4305"
assert get_mask_account(1234567890) == "**7890"


def test_get_mask_account_invalid() -> None:
    """Тест: если введен некорректный номер карты"""
    # Проверяем, что функция выведет ошибку при некорректном вводе номера карты
    with pytest.raises(ValueError):
        get_mask_account(123)  # Введено только 3 цифры. Необходимо ввести минимум 4
