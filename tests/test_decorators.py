import os
import pytest

from src.decorators import log

# ============================================================
# Фикстуры
# ============================================================


@pytest.fixture
def log_file(tmp_path):
    """Возвращает путь к временному файлу для логов."""
    return tmp_path / "test_log.txt"


@pytest.fixture
def read_log(log_file):
    """Возвращает функцию для чтения содержимого лог-файла."""

    def _read():
        with open(log_file, "r", encoding="utf-8") as f:
            return f.read()

    return _read


# ============================================================
# Тесты логирования в файл — успешное выполнение
# ============================================================


def test_log_to_file_success_no_args(log_file, read_log):
    """Успешное выполнение функции без аргументов — лог в файл."""

    @log(filename=str(log_file))
    def my_function():
        return 42

    result = my_function()

    assert result == 42
    assert read_log() == "my_function ok\n"


def test_log_to_file_success_with_args(log_file, read_log):
    """Успешное выполнение функции с позиционными аргументами."""

    @log(filename=str(log_file))
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)

    assert result == 3
    assert read_log() == "my_function ok\n"


def test_log_to_file_success_with_kwargs(log_file, read_log):
    """Успешное выполнение функции с именованными аргументами."""

    @log(filename=str(log_file))
    def my_function(x, y):
        return x * y

    result = my_function(x=3, y=4)

    assert result == 12
    assert read_log() == "my_function ok\n"


def test_log_to_file_appends_multiple_calls(log_file, read_log):
    """Несколько вызовов функции — логи дописываются в файл."""

    @log(filename=str(log_file))
    def my_function(x):
        return x

    my_function(1)
    my_function(2)
    my_function(3)

    assert read_log() == "my_function ok\nmy_function ok\nmy_function ok\n"


def test_log_creates_file_if_not_exists(log_file):
    """Файл лога создаётся, если его не существует."""
    assert not os.path.exists(log_file)

    @log(filename=str(log_file))
    def my_function():
        return "done"

    my_function()

    assert os.path.exists(log_file)


# ============================================================
# Тесты логирования в файл — обработка исключений
# ============================================================


def test_log_to_file_error_no_args(log_file, read_log):
    """Ошибка в функции без аргументов — лог с типом ошибки."""

    @log(filename=str(log_file))
    def my_function():
        raise ValueError("something went wrong")

    with pytest.raises(ValueError):
        my_function()

    assert read_log() == "my_function error: ValueError. Inputs: (), {}\n"


def test_log_to_file_error_with_args(log_file, read_log):
    """Ошибка в функции с позиционными аргументами."""

    @log(filename=str(log_file))
    def my_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    assert read_log() == ("my_function error: ZeroDivisionError. Inputs: (1, 0), {}\n")


def test_log_to_file_error_with_kwargs(log_file, read_log):
    """Ошибка в функции с именованными аргументами."""

    @log(filename=str(log_file))
    def my_function(x, y):
        raise TypeError("wrong types")

    with pytest.raises(TypeError):
        my_function(x=1, y=2)

    assert read_log() == ("my_function error: TypeError. Inputs: (), {'x': 1, 'y': 2}\n")


def test_log_to_file_error_with_mixed_args(log_file, read_log):
    """Ошибка в функции со смешанными аргументами."""

    @log(filename=str(log_file))
    def my_function(a, b, c=10):
        raise KeyError("missing")

    with pytest.raises(KeyError):
        my_function(1, 2, c=3)

    assert read_log() == ("my_function error: KeyError. Inputs: (1, 2), {'c': 3}\n")


def test_log_error_propagates_exception(log_file):
    """Исключение пробрасывается дальше после логирования."""

    @log(filename=str(log_file))
    def my_function():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        my_function()


# ============================================================
# Тесты логирования в консоль (с фикстурой capsys)
# ============================================================


def test_log_to_console_success(capsys):
    """Успешное выполнение — лог в консоль."""

    @log()
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)

    assert result == 3
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


def test_log_to_console_success_no_filename_arg(capsys):
    """Декоратор без аргументов вообще — лог в консоль."""

    @log
    def my_function():
        return 1

    my_function()

    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


def test_log_to_console_error(capsys):
    """Ошибка — лог в консоль с типом ошибки и аргументами."""

    @log()
    def my_function(x, y):
        raise ValueError("bad input")

    with pytest.raises(ValueError):
        my_function(1, 2)

    captured = capsys.readouterr()
    assert captured.out == "my_function error: ValueError. Inputs: (1, 2), {}\n"


def test_log_to_console_error_with_kwargs(capsys):
    """Ошибка с именованными аргументами — лог в консоль."""

    @log()
    def my_function(a, b):
        raise ArithmeticError("math error")

    with pytest.raises(ArithmeticError):
        my_function(a=5, b=6)

    captured = capsys.readouterr()
    assert captured.out == ("my_function error: ArithmeticError. Inputs: (), {'a': 5, 'b': 6}\n")


def test_log_to_console_multiple_calls(capsys):
    """Несколько вызовов — несколько строк в консоли."""

    @log()
    def my_function():
        return 0

    my_function()
    my_function()

    captured = capsys.readouterr()
    assert captured.out == "my_function ok\nmy_function ok\n"


# ============================================================
# Тесты корректности возвращаемого значения и метаданных
# ============================================================


def test_log_returns_original_result(capsys):
    """Декоратор возвращает результат оригинальной функции."""

    @log()
    def my_function(x):
        return {"result": x * 2}

    assert my_function(5) == {"result": 10}


def test_log_preserves_function_metadata():
    """functools.wraps сохраняет имя и docstring функции."""

    @log()
    def my_function():
        """Моя документация."""
        return None

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Моя документация."


def test_log_different_functions_use_different_names(log_file, read_log):
    """Имя функции в логе соответствует вызванной функции."""

    @log(filename=str(log_file))
    def first_function():
        return 1

    @log(filename=str(log_file))
    def second_function():
        return 2

    first_function()
    second_function()

    assert read_log() == "first_function ok\nsecond_function ok\n"


def test_log_error_logs_inputs_for_multiple_calls(log_file, read_log):
    """Каждый ошибочный вызов логируется с собственными аргументами."""

    @log(filename=str(log_file))
    def my_function(x):
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        my_function(1)
    with pytest.raises(RuntimeError):
        my_function(2)

    expected = (
        "my_function error: RuntimeError. Inputs: (1,), {}\n" "my_function error: RuntimeError. Inputs: (2,), {}\n"
    )
    assert read_log() == expected
