from src.ecommerce.models import Category, Product

"""Тесты классов Product и Category."""


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
    Category("A", "d", sample_products)                    # +3
    Category("B", "d", [])                                 # +0
    Category("C", "d", [sample_products[0]])               # +1
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
