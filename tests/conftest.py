import pytest

# ======= ФИКСТУРЫ ДЛЯ ТЕСТА MASKS.PY =======


@pytest.fixture
def valid_card_numbers():
    """Валидные 16-значные номера карт"""
    return [
        7000792289606361,
        7158300734726758,
        6831982476737658,
        1234567890123456,
    ]


@pytest.fixture
def invalid_card_numbers():
    """Невалидные номера карт"""
    return [
        12345,  # 5 цифр
        123456789012345,  # 15 цифр
        12345678901234567,  # 17 цифр
        0,  # 1 цифра
    ]


@pytest.fixture
def valid_account_numbers():
    """Валидные номера счетов (минимум 4 цифры)"""
    return [
        64686473678894779589,
        35383033474447895560,
        73654108430135874305,
        1234,  # минимальный (4 цифры)
        1234567890,
    ]


@pytest.fixture
def invalid_account_numbers():
    """Невалидные номера счетов"""
    return [
        1,    # Одна цифра
        12,   # Две цифры
        123,  # Три цифры
    ]


# ========== ФИКСТУРЫ ДЛЯ WIDGET.PY ==========


@pytest.fixture
def transaction_strings():
    """Строки с транзакциями для тестирования mask_account_card."""
    return [
        "Maestro 1596837868705199",
        "Visa Platinum 7000792289606361",
        "MasterCard 7158300734726758",
        "Visa Classic 6831982476737658",
        "Счет 73654108430135874305",
        "Счет 64686473678894779589",
        "Счет 35383033474447895560",
    ]


@pytest.fixture
def date_strings():
    """Строки с датами для тестирования get_date."""
    return [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2024-01-01T00:00:00.000000",
        "2019-08-26T10:50:58.294041",
        "2020-03-23T11:45:00.000000",
    ]


@pytest.fixture
def invalid_transaction_strings():
    """Невалидные строки для тестирования обработки ошибок."""
    return [
        "",  # пустая строка
        "   ",  # только пробелы
        "Карта",  # нет номера
        "Счет 123",  # слишком короткий номер
        "Visa Platinum abc123",  # не цифры в номере
        "1234567890123456",  # только цифры, без типа
    ]


# ========== ФИКСТУРЫ ДЛЯ PROCESSING.PY ==========


@pytest.fixture
def sample_transactions():
    """Тестовые транзакции для обработки."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-11-30T15:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-02T09:15:00.000000"},
        {"id": 4, "state": "CANCELED", "date": "2023-11-29T18:45:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-11-28T14:20:00.000000"},
    ]


@pytest.fixture
def transactions_without_state():
    """Транзакции без поля state для тестирования обработки ошибок."""
    return [
        {"id": 1, "date": "2023-12-01T12:00:00.000000"},
        {"id": 2, "date": "2023-11-30T15:30:00.000000"},
    ]


@pytest.fixture
def unsorted_transactions():
    """Транзакции в разном порядке для тестирования сортировки."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-12-03T10:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2023-11-30T15:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-01T09:15:00.000000"},
        {"id": 4, "state": "EXECUTED", "date": "2023-12-02T14:45:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-11-29T18:20:00.000000"},
    ]


@pytest.fixture
def empty_transactions():
    """Пустой список транзакций."""
    return []


@pytest.fixture
def single_transaction():
    """Одна транзакция для граничных случаев."""
    return [{"id": 1, "state": "EXECUTED", "date": "2023-12-01T12:00:00.000000"}]
