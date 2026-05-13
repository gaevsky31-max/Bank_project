"""
Тесты для модуля utils.
"""

import json

from src.utils import read_json_file


def test_read_json_file_success(tmp_path):
    """Тест: успешное чтение JSON файла."""
    test_file = tmp_path / "normal.json"
    test_data = [{"id": 1, "amount": 100}]

    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result = read_json_file(str(test_file))
    assert result == test_data


def test_read_json_file_empty(tmp_path):
    """Тест: пустой файл."""
    test_file = tmp_path / "empty.json"
    test_file.touch()

    result = read_json_file(str(test_file))
    assert result == []


def test_read_json_file_dict(tmp_path):
    """Тест: файл со словарём (не список)."""
    test_file = tmp_path / "dict.json"

    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump({"key": "value"}, f)

    result = read_json_file(str(test_file))
    assert result == []


def test_read_json_file_not_found():
    """Тест: файл не найден."""
    result = read_json_file("non_existent_12345.json")
    assert result == []


def test_read_json_file_invalid(tmp_path):
    """Тест: повреждённый JSON."""
    test_file = tmp_path / "invalid.json"

    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("this is not json {")

    result = read_json_file(str(test_file))
    assert result == []
