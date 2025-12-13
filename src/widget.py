from . import masks


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в передаваемой строке.

    Args:
        account_info (str): Строка с типом, номером карты или счета.
            Пример: Visa Platinum 7000792289606361, Maestro 7000792289606361 или
            Счет 73654108430135874305.

    Returns:
        str: Строка с замаскированным номером карты или счета.
    """

    parts = account_info.split()
    if len(parts) < 2:
        return account_info

    card_type = " ".join(parts[:-1])
    number_str = parts[-1]

    # Проверяем что строка состоит только из цифр
    if not number_str.isdigit():
        return account_info

    if card_type.lower() == "счет":
        try:
            # Преобразуем строку в int для masks.py
            number_int = int(number_str)
            masked_number = masks.get_mask_account(number_int)
        except ValueError:
            return account_info
    else:
        try:
            number_int = int(number_str)
            masked_number = masks.get_mask_card_number(number_int)
        except ValueError:
            return account_info

    return f"{card_type} {masked_number}"


def get_date(date_info: str) -> str:
    """
    Функция преобразует формат даты.

    Args:
        date_info (str): Дата в формате: "2024-03-11T02:26:18.671407"

    Returns:
        str: Дата в формате: "11.03.2024" или исходная строка при ошибке
    """
    try:
        date_str = date_info.split("T")[0]
        year, month, day = date_str.split("-")
        return f"{day}.{month}.{year}"
    except (ValueError, IndexError):
        # Возвращаем исходную строку если не можем распарсить
        return date_info
