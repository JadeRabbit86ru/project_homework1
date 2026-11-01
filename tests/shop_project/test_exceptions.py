from src.shop_project import ZeroQuantityError


def test_zero_quantity_error_is_value_error():
    assert issubclass(ZeroQuantityError, ValueError)


def test_zero_quantity_error_default_message():
    error = ZeroQuantityError()
    assert str(error) == "Товар с нулевым количеством не может быть добавлен"


def test_zero_quantity_error_custom_message():
    error = ZeroQuantityError("Другое сообщение")
    assert str(error) == "Другое сообщение"
