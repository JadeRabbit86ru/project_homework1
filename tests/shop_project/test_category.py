import pytest

from src.shop_project import Product, Category


def test_category_init(category):
    assert category.name == "Смартфоны"
    assert len(category) == 2


def test_products_property(category):
    text = category.products
    assert "Samsung Galaxy S23 Ultra" in text
    assert "Iphone 15" in text
    assert "руб." in text


def test_add_product_valid(category, smartphone1):
    before = len(category)
    category.add_product(smartphone1)
    assert len(category) == before + 1


def test_add_product_plain_product_is_allowed(category):
    p = Product("Обычный товар", "d", 10.0, 1)
    category.add_product(p)
    assert len(category) == 3


def test_add_product_invalid_raises(category):
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_add_product_invalid_int_raises(category):
    with pytest.raises(TypeError):
        category.add_product(42)


def test_product_count_increases(smartphone1):
    from src.shop_project import Category

    Category.product_count = 0
    Category("A", "d", [smartphone1])
    Category("B", "d", [smartphone1])
    assert Category.product_count == 2


"""Работа 17.1"""


def test_average_price_with_products(category):
    # category создаётся из smartphone1 + smartphone2
    expected = (180000.0 + 210000.0) / 2
    assert category.average_price() == expected


def test_average_price_empty_category():
    empty = Category("Пустая", "Нет товаров", [])
    assert empty.average_price() == 0
