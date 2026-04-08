"""
Тесты для декоратора log.
"""

import os
import tempfile

import pytest

from src.decorators import log


def test_log_to_console(capsys):
    """Тест логирования в консоль при успешном выполнении."""

    @log()
    def test_func():
        return "success"

    result = test_func()
    captured = capsys.readouterr()

    assert result == "success"
    assert "Функция test_func успешно выполнена. Результат: success" in captured.out
    assert "Время:" in captured.out


def test_log_with_arguments(capsys):
    """Тест логирования функции с аргументами."""

    @log()
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)
    captured = capsys.readouterr()

    assert result == 20
    assert "Функция multiply успешно выполнена. Результат: 20" in captured.out


def test_log_to_file():
    """Тест логирования в файл."""

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False) as tmp_file:
        filename = tmp_file.name

    try:
        @log(filename=filename)
        def test_func():
            return "file_log"

        result = test_func()
        assert result == "file_log"

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Функция test_func успешно выполнена. Результат: file_log" in content
            assert "Время:" in content

    finally:
        os.unlink(filename)


def test_log_exception_to_console(capsys):
    """Тест логирования исключения в консоль."""

    @log()
    def failing_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        failing_func()

    captured = capsys.readouterr()
    assert "Функция failing_func завершилась с ошибкой ValueError" in captured.out
    assert "Входные параметры: args=(), kwargs={}" in captured.out


def test_log_exception_to_file():
    """Тест логирования исключения в файл."""

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False) as tmp_file:
        filename = tmp_file.name

    try:
        @log(filename=filename)
        def failing_func(x):
            if x < 0:
                raise ValueError("Negative value")
            return x

        with pytest.raises(ValueError, match="Negative value"):
            failing_func(-5)

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Функция failing_func завершилась с ошибкой ValueError" in content
            assert "Входные параметры: args=(-5,), kwargs={}" in content

    finally:
        os.unlink(filename)


def test_add_function(capsys):
    """Тест функции add из модуля decorators."""
    from src.decorators import add

    result = add(3, 7)
    captured = capsys.readouterr()

    assert result == 10
    assert "Функция add успешно выполнена. Результат: 10" in captured.out


def test_divide_success(capsys):
    """Тест успешного выполнения divide."""
    from src.decorators import divide

    result = divide(10, 2)
    captured = capsys.readouterr()

    assert result == 5.0
    assert "Функция divide успешно выполнена. Результат: 5.0" in captured.out


def test_divide_by_zero():
    """Тест деления на ноль с логированием в файл."""

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False) as tmp_file:
        filename = tmp_file.name

    try:
        # Создаем новую функцию с логированием в файл
        @log(filename=filename)
        def test_divide(a, b):
            if b == 0:
                raise ValueError("Деление на ноль")
            return a / b

        with pytest.raises(ValueError, match="Деление на ноль"):
            test_divide(10, 0)

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Функция test_divide завершилась с ошибкой ValueError" in content
            assert "Входные параметры: args=(10, 0), kwargs={}" in content

    finally:
        os.unlink(filename)


def test_decorator_preserves_function_metadata():
    """Тест сохранения метаданных функции после декорирования."""

    @log()
    def test_func():
        """Test docstring."""
        return "test"

    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Test docstring."


def test_multiple_calls_to_file(capsys):
    """Тест множественных вызовов одной функции с логированием в консоль."""

    @log()
    def counter():
        return 1

    counter()
    counter()
    captured = capsys.readouterr()

    # Проверяем, что оба вызова залогированы
    assert captured.out.count("Функция counter успешно выполнена") == 2


def test_log_with_different_exception_types(capsys):
    """Тест логирования разных типов исключений."""

    @log()
    def type_error_func():
        return "string" + 5

    with pytest.raises(TypeError):
        type_error_func()

    captured = capsys.readouterr()
    assert "Функция type_error_func завершилась с ошибкой TypeError" in captured.out
