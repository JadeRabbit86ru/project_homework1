import pytest

from src.shop_project import Product, BaseProduct


def test_product_init(product):
    assert product.name == "Товар"
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 10


def test_product_add_same_class():
    p1 = Product("A", "d", 100.0, 2)
    p2 = Product("B", "d", 50.0, 3)
    assert p1 + p2 == 100.0 * 2 + 50.0 * 3


def test_product_add_different_classes_raises(smartphone1, grass1):
    with pytest.raises(TypeError):
        _ = smartphone1 + grass1


def test_product_add_with_subclass_raises(product, smartphone1):
    with pytest.raises(TypeError):
        _ = product + smartphone1


def test_product_is_baseproduct_subclass():
    assert issubclass(Product, BaseProduct)


def test_baseproduct_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("A", "d", 100.0, 1)


"""Работа 17.1"""

from src.shop_project import Product, ZeroQuantityError


def test_product_zero_quantity_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        Product("Товар", "Описание", 100.0, 0)
    assert str(excinfo.value) == "Товар с нулевым количеством не может быть добавлен"


def test_product_negative_quantity_raises():
    with pytest.raises(ValueError):
        Product("Товар", "Описание", 100.0, -1)


def test_product_zero_quantity_is_zero_quantity_error():
    with pytest.raises(ZeroQuantityError):
        Product("Товар", "Описание", 100.0, 0)
