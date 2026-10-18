import pytest

from src.ecommerce.models import Category
from src.ecommerce.models import Product


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики класса перед каждым тестом — изоляция."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    return [
        Product("Samsung Galaxy C23 Ultra", "256GB", 180_000.0, 5),
        Product("Iphone 15", "512GB", 210_000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB", 31_000.0, 14),
    ]
