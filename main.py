""" Демонстрация функционала"""

from src.masks import get_mask_card_number, get_mask_account
# Импортируем наши функции из модуля masks

def main() -> None:
    # Функция main точка входа в программу

    # Пример с номером карты
    card_number = 7000792289606361
    masked_card_number = get_mask_card_number(card_number) # вызываем функцию маскировки
    print(f"card: {card_number} -> {masked_card_number}")
    # Выведет Card: 7000792289606361 -> 7000 79** **** 6361

    # Пример с номером счета
    account_number = 73654108430135874305
    masked_account_number = get_mask_account(account_number)
    print(f"Account: {account_number} -> {masked_account_number}")
    # Выведет Account: 73654108430135874305 -> **4305

if __name__ == "__main__":
    main()