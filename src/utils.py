"""
Модуль с утилитами для работы с данными.
"""

import json
from typing import Any
from typing import Dict
from typing import List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей или пустой список при ошибке.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            else:
                return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        return []
