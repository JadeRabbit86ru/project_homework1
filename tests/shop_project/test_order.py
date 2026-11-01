import pytest

from src.shop_project import BaseInfo, Order


def test_order_is_baseinfo_subclass():
    assert issubclass(Order, BaseInfo)


def test_order_creation(smartphone1):
    order = Order(smartphone1, 2)
    assert order.product is smartphone1
    assert order.quantity == 2
    assert order.total_price == smartphone1.price * 2


def test_order_str(smartphone1):
    order = Order(smartphone1, 1)
    text = str(order)
    assert "Samsung Galaxy S23 Ultra" in text
    assert "1" in text
    assert "180000.0" in text


def test_order_invalid_product_raises():
    with pytest.raises(TypeError):
        Order("Not a product", 1)


def test_order_quantity_nonpositive_raises(smartphone1):
    with pytest.raises(ValueError):
        Order(smartphone1, 0)


def test_order_quantity_too_large_raises(smartphone1):
    with pytest.raises(ValueError):
        Order(smartphone1, smartphone1.quantity + 1)


def test_order_accepts_plain_product(product):
    order = Order(product, 3)
    assert order.total_price == product.price * 3


"""Работа 17.1"""

from src.shop_project import ZeroQuantityError


def test_zero_quantity_error_is_value_error():
    assert issubclass(ZeroQuantityError, ValueError)


def test_zero_quantity_error_default_message():
    error = ZeroQuantityError()
    assert str(error) == "Товар с нулевым количеством не может быть добавлен"


def test_zero_quantity_error_custom_message():
    error = ZeroQuantityError("Другое сообщение")
    assert str(error) == "Другое сообщение"
