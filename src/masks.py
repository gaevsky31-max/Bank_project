"""Модуль для маскировки банковской карты и счета"""

import logging
import os

# Настройка логера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Функция маскирует номер карты в формате: XXXX XX** **** XXXX

    Args:
       card_number(int): Номер карты в виде целого числа

    Returns:
       str: Замаскированный номер карты в виде: XXXX XX** **** XXXX.
    """
    card_str = str(card_number)

    if len(card_str) != 16:
        logger.error(f"Ошибка: номер карты должен содержать 16 цифр, получено {len(card_str)}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    # Логируем успешный результат
    logger.info(f"Успешно замаскирован номер карты: {masked_card}")

    return masked_card


def get_mask_account(account_number: int) -> str:
    """
    Функция маскирует номер счета в формате: **XXXX

    Args:
       account_number(int): Номер счета в виде целого числа

    Returns:
       str: Замаскированный номер счета в виде: **XXXX.
    """
    account_str = str(account_number)

    if len(account_str) < 4:
        logger.error(f"Ошибка: номер счета должен содержать минимум 4 цифры, получено {len(account_str)}")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    masked_account = f"**{account_str[-4:]}"

    # Логируем успешный результат
    logger.info(f"Успешно замаскирован номер счета: {masked_account}")

    return masked_account
