from typing import Any
from typing import Dict
from typing import List


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Функция фильтрует список операций по статусу

    Args:
        operations (List[Dict[str, Any]]): список словарей с данными о банковских операциях.
        state (str): Статус операции для фильтрации (по умолчанию 'EXECUTED').
    Returns:
        List[Dict[str, Any]]: Отфильтрованный список операций
    """
    filtered_operations = []
    for operation in operations:
        if operation.get('state') == state:
            filtered_operations.append(operation)
    return filtered_operations


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Функция сортирует банковские операции по дате.

    Args:
        operations: (List[Dict[str, Any]]): список словарей с данными о банковских операциях.
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию).
    Returns:
         List[Dict[str, Any]]: Отфильтрованный список операций по дате.
    """
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=reverse)
