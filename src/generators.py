"""
Модуль с функциями-генераторами для обработки транзакций.
Содержит генераторы для фильтрации по валюте, получения описаний и генерации номеров карт.
"""

from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterator
from typing import List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str = "USD") -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (по умолчанию "USD")

    Yields:
        Транзакции с указанной валютой.

    Examples:
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> for _ in range(2):
        ...     print(next(usd_transactions))
    """
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency:
                yield transaction
        except KeyError:
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, возвращающий описание транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой транзакции

    Examples:
        >>> descriptions = transaction_descriptions(transactions)
        >>> for _ in range(5):
        ...     print(next(descriptions))
    """
    for transaction in transactions:
        # ИСПРАВЛЕНО: "description" а не "descriptions"
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение диапазона (от 1 до 9999999999999999)
        stop: Конечное значение диапазона (включительно)

    Yields:
        Номер карты в формате: XXXX XXXX XXXX XXXX

    Examples:
        >>> for card_number in card_number_generator(1, 5):
        ...     print(card_number)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
        0000 0000 0000 0004
        0000 0000 0000 0005

    Raises:
        ValueError: Если номера карт выходят за допустимые пределы
    """
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Номер карты должен быть в диапазоне от 1 до 9999999999999999")

    for number in range(start, stop + 1):
        # Форматируем номер: 16 цифр с пробелами каждые 4 цифры
        card_number = f"{number:016d}"  # желтое подчеркивание можно игнорировать
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
        yield formatted_number
