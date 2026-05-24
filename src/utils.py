"""
Модуль с утилитами для работы с данными.
"""

import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List

# Настройка логера для модуля Utils.py
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler("logs/utils.log", mode='w', encoding='utf-8')

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей или пустой список при ошибке.
    """
    logger.debug(f"Попытка открыть файл: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.debug(f"Файл успешно прочитан: {file_path}")

            if isinstance(data, list):
                logger.info(f"Файл {file_path} содержит список из: {len(data)} элементов")
                return data
            else:
                logger.warning(f"Файл {file_path} содержит не список, а: {type(data).__name__}")
                return []

    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла: {file_path}: {e}")
        return []
