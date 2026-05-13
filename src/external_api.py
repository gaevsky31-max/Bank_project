"""
Модуль для работы с внешним API конвертации валют.
"""

import os
from typing import Any
from typing import Dict
from typing import Optional

import requests
from dotenv import load_dotenv

# Загружаем .env из корня проекта (папкой выше)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# API ключ
API_KEY = os.getenv("EXCHANGE_API_KEY")

# Проверка для отладки (потом можно удалить)
print(f"DEBUG: Загружаю .env из {dotenv_path}")
print(f"DEBUG: API_KEY = {API_KEY}")

BASE_URL = "https://api.currencyapi.com/v3"


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции.
            Должен содержать ключи "amount" и "currency".

    Returns:
        float: Сумма транзакции в рублях.

    Examples:
        >>> transaction = {"amount": 100, "currency": "USD"}
        >>> convert_to_rub(transaction)
        9150.0

        >>> transaction = {"amount": 5000, "currency": "RUB"}
        >>> convert_to_rub(transaction)
        5000.0
    """
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB")

    # Преобразуем сумму в число
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return 0.0

    # Если валюта уже рубли
    if currency == "RUB":
        return amount

    # Если валюта USD или EUR, конвертируем
    if currency in ["USD", "EUR"]:
        rate = get_exchange_rate(currency)
        if rate:
            return round(amount * rate, 2)
        else:
            return 0.0

    # Для других валют возвращаем 0
    return 0.0


def get_exchange_rate(currency: str) -> Optional[float]:
    """
    Получает текущий курс валюты к рублю через CurrencyAPI.

    Args:
        currency (str): Код валюты ("USD" или "EUR").

    Returns:
        Optional[float]: Курс валюты к рублю, или None если ошибка.

    Examples:
        >>> rate = get_exchange_rate("USD")
        >>> print(rate)
        91.50
    """
    # Проверяем наличие API ключа
    if not API_KEY:
        print("Ошибка: API ключ не найден. Установите EXCHANGE_API_KEY в .env файле")
        return None

    # Формируем параметры запроса
    url = f"{BASE_URL}/latest"
    params = {
        "apikey": API_KEY,
        "base_currency": currency,
        "currencies": "RUB"
    }

    try:
        # Отправляем запрос к API
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Парсим JSON ответ
        data = response.json()

        # Извлекаем курс из ответа
        # Структура ответа: {"data": {"RUB": {"code": "RUB", "value": 91.50}}}
        if "data" in data and "RUB" in data["data"]:
            rate = data["data"]["RUB"]["value"]
            return float(rate)
        else:
            print(f"Ошибка: Неожиданный формат ответа от API: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return None
