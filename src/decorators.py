"""
Модуль с декораторами для логирования работы функций.
"""

from datetime import datetime
from functools import wraps


def log(filename=None):
    """
    Декоратор для логирования вызова функций.

    Автоматически логирует начало и конец выполнения функции,
    результат выполнения или возникшие ошибки.

    Args:
        filename (str, optional): Имя файла для записи логов.
            Если не указан, логи выводятся в консоль.

    Returns:
        function: Декорированная функция.

    Example:
        @log()
        def add(a, b):
            return a + b

        @log("app.log")
        def divide(a, b):
            return a / b
    """

    def my_decorator(func):
        """
        Внутренний декоратор, который оборачивает функцию.

        Args:
            func (callable): Функция для декорирования.

        Returns:
            callable: Обёрнутая функция.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обёртка, которая выполняет логирование до и после вызова функции.

            Args:
                *args: Позиционные аргументы функции.
                **kwargs: Именованные аргументы функции.

            Returns:
                Any: Результат выполнения оригинальной функции.

            Raises:
                Exception: Перевыбрасывает любое исключение,
                          возникшее в оригинальной функции.
            """
            start_time = datetime.now()
            timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')

            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                log_message = (
                    f"{timestamp} - Функция {func.__name__} успешно выполнена. "
                    f"Результат: {result}. Время: {duration:.3f}с\n"
                )

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                log_message = (
                    f"{timestamp} - Функция {func.__name__} завершилась с ошибкой "
                    f"{type(e).__name__}. Входные параметры: args={args}, kwargs={kwargs}\n"
                )

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")
                raise

        return wrapper

    return my_decorator


# Примеры использования декоратора
@log()
def add(a: int, b: int) -> int:
    """
    Сложение двух чисел.

    Args:
        a (int): Первое число.
        b (int): Второе число.

    Returns:
        int: Сумма чисел.
    """
    return a + b


@log()
def divide(a: float, b: float) -> float:
    """
    Деление двух чисел.

    Args:
        a (float): Делимое.
        b (float): Делитель.

    Returns:
        float: Частное от деления.

    Raises:
        ValueError: Если делитель равен нулю.
    """
    if b == 0:
        raise ValueError("Деление на ноль")
    return a / b
