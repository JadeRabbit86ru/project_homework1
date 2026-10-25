"""Тесты классов Product и Category."""

from src.ecommerce.models import Category
from src.ecommerce.models import Product

# ---------- Product ----------


def test_product_init():
    p = Product("Iphone 15", "512GB, Gray space", 210_000.0, 8)
    assert p.name == "Iphone 15"
    assert p.description == "512GB, Gray space"
    assert p.price == 210_000.0
    assert p.quantity == 8


def test_product_types():
    p = Product("Test", "Desc", 99.99, 1)
    assert isinstance(p.name, str)
    assert isinstance(p.price, float)
    assert isinstance(p.quantity, int)


# ---------- Category ----------


def test_category_init(sample_products):
    cat = Category("Смартфоны", "Описание", sample_products)
    assert cat.name == "Смартфоны"
    assert cat.description == "Описание"
    assert cat.products == sample_products
    assert all(isinstance(p, Product) for p in cat.products)


def test_category_empty_products():
    cat = Category("Пустая", "Нет товаров", [])
    assert cat.products == []


# ---------- Счётчики ----------


def test_product_count_accumulates(sample_products):
    Category("A", "d", sample_products)  # +3
    Category("B", "d", [])  # +0
    Category("C", "d", [sample_products[0]])  # +1
    assert Category.product_count == 4


def test_category_count_increments(sample_products):
    assert Category.category_count == 0
    Category("A", "d", sample_products)
    assert Category.category_count == 1
    Category("B", "d", [])
    assert Category.category_count == 2


def test_counters_shared_across_instances(sample_products):
    c1 = Category("A", "d", sample_products)
    c2 = Category("B", "d", [])
    # доступ через экземпляр также виден
    assert c1.category_count == 2
    assert c2.product_count == 3


"""Работа 14.2"""


# --- Product ---


def test_product_init2(sample_product):
    assert sample_product.name == "Яблоко"
    assert sample_product.price == 80
    assert sample_product.quantity == 15


def test_price_getter(sample_product):
    assert sample_product.price == 80


def test_price_setter_valid(sample_product, monkeypatch):
    # Подменяем input, чтобы не блокировать тест, если сработает доп. задание
    monkeypatch.setattr("builtins.input", lambda _: "y")
    sample_product.price = 100
    assert sample_product.price == 100


def test_price_setter_invalid(sample_product, capsys):
    sample_product.price = -10
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 80  # Цена не изменилась


def test_new_product_create():
    data = {"name": "Банан", "description": "Желтый", "price": 50, "quantity": 10}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Банан"
    assert p.price == 50


def test_new_product_merge_duplicates(sample_product):
    products = [sample_product]  # В списке уже есть Яблоко (цена 80, кол-во 15)
    data = {"name": "Яблоко", "description": "Свежее", "price": 90, "quantity": 5}
    merged = Product.new_product(data, products)

    assert merged.quantity == 20  # 15 + 5
    assert merged.price == 90  # Выбрана максимальная цена


# --- Тесты для Category ---


def test_category_init2(sample_category):
    assert sample_category.name == "Фрукты"
    assert sample_category.products == ""  # Изначально пусто


def test_add_product(sample_category, sample_product):
    initial_count = Category.product_count
    sample_category.add_product(sample_product)

    assert Category.product_count == initial_count + 1
    expected_str = "Яблоко, 80 руб. Остаток: 15 шт.\n"
    assert sample_category.products == expected_str


def test_products_getter_multiple(sample_category, sample_product):
    p2 = Product("Груша", "Сладкая", 60, 20)
    sample_category.add_product(sample_product)
    sample_category.add_product(p2)

    expected = "Яблоко, 80 руб. Остаток: 15 шт.\nГруша, 60 руб. Остаток: 20 шт.\n"
    assert sample_category.products == expected


"""Работа 15.1"""


def test_product_str():
    p = Product("Test", "Desc", 100.0, 5)
    assert str(p) == "Test, 100.0 руб. Остаток: 5 шт."


def test_category_str():
    p1 = Product("A", "Desc", 100.0, 5)
    p2 = Product("B", "Desc", 200.0, 10)
    cat = Category("TestCat", "Desc", [p1, p2])
    # Общее количество: 5 + 10 = 15
    assert str(cat) == "TestCat, количество продуктов: 15 шт."


def test_product_add():
    p1 = Product("A", "Desc", 100.0, 10)  # 1000
    p2 = Product("B", "Desc", 200.0, 2)  # 400
    assert p1 + p2 == 1400.0
