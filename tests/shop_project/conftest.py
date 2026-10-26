import pytest

from src.shop_project import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def product():
    return Product("Товар", "Описание", 100.0, 10)


@pytest.fixture
def smartphone1():
    return Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
        180000.0, 5, 95.5, "S23 Ultra", 256, "Серый",
    )


@pytest.fixture
def smartphone2():
    return Smartphone(
        "Iphone 15", "512GB, Gray space",
        210000.0, 8, 98.2, "15", 512, "Gray space",
    )


@pytest.fixture
def grass1():
    return LawnGrass(
        "Газонная трава", "Элитная трава для газона",
        500.0, 20, "Россия", "7 дней", "Зеленый",
    )


@pytest.fixture
def grass2():
    return LawnGrass(
        "Газонная трава 2", "Выносливая трава",
        450.0, 15, "США", "5 дней", "Темно-зеленый",
    )


@pytest.fixture
def category(smartphone1, smartphone2):
    return Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
