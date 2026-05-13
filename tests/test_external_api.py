"""
Тесты для модуля external_api.
"""

from unittest.mock import Mock, patch

import requests
from src.external_api import convert_to_rub, get_exchange_rate


def test_convert_to_rub():
    """Тест: транзакция уже в рублях."""
    transaction = {"amount": 100, "currency": "RUB"}
    assert convert_to_rub(transaction) == 100.0


def test_convert_usd():
    """Тест: конвертация USD в рубли."""
    transaction = {"amount": 100, "currency": "USD"}
    with patch('src.external_api.get_exchange_rate', return_value=95.00):
        assert convert_to_rub(transaction) == 9500.0


def test_invalid_amount():
    """Тест: невалидная сумма."""
    transaction = {"amount": "abc", "currency": "USD"}
    assert convert_to_rub(transaction) == 0.0


def test_unknown_currency():
    """Тест: неизвестная валюта."""
    transaction = {"amount": 100, "currency": "GBP"}
    assert convert_to_rub(transaction) == 0.0


def test_get_rate_success():
    """Тест: успешное получение курса."""
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"RUB": {"value": 95.50}}}
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        with patch('src.external_api.API_KEY', 'test_key'):
            rate = get_exchange_rate("USD")
            assert rate == 95.50


def test_get_rate_no_key():
    """Тест: отсутствие API ключа."""
    with patch('src.external_api.API_KEY', None):
        assert get_exchange_rate("USD") is None


def test_get_rate_api_error():
    """Тест: ошибка сети при запросе."""
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError("error")):
        with patch('src.external_api.API_KEY', 'test_key'):
            assert get_exchange_rate("USD") is None
