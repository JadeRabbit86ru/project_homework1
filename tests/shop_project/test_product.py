import pytest

from src.shop_project import Product


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
