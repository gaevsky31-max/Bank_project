""" Тест для widget.py"""

from src.widget import get_date
from src.widget import mask_account_card


def test_mask_account_card() -> None:
    """Тестируем функцию маскировки номера карты/счета"""
    # Тест для карт
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"

    # Тест для счетов
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"
    assert mask_account_card("Счет 35383033474447895560") == "Счет **5560"


def test_get_date() -> None:
    """Тестируем преобразование формата даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-12-31T23:59:59.999999") == "31.12.2023"
    assert get_date("2024-01-01T00:00:00.000000") == "01.01.2024"


if __name__ == "__main__":
    test_mask_account_card()
    test_get_date()
print("Все тесты пройдены")
