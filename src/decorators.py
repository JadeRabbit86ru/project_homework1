import functools


def log(filename=None):
    """
    Декоратор для логирования выполнения функции.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}"
                _write_log(message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message, filename=None):
    """Вспомогательная функция для записи лога в файл или консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
