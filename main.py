from pathlib import Path

from src.ecommerce.json_loader import load_categories_from_json
from src.ecommerce.models import Category, Product

"""Точка входа: демонстрация работы классов и загрузки из JSON."""


def demo() -> None:
    """Демонстрация функционала."""
    # Ручное создание объектов
    p1 = Product("Iphone 15", "512GB, Gray space", 210_000.0, 8)
    p2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31_000.0, 14)
    cat = Category("Смартфоны", "Средство коммуникации", [p1, p2])

    print(f"Категория: {cat.name}, товаров в ней: {len(cat.products)}")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров:   {Category.product_count}")

    # Загрузка из JSON
    json_path = Path(__file__).parent / "products.json"
    if json_path.exists():
        cats = load_categories_from_json(json_path)
        print(f"\nЗагружено из JSON категорий: {len(cats)}")
        for c in cats:
            print(f" - {c.name}: {len(c.products)} товар(ов)")


if __name__ == "__main__":
    demo()
