# Код из прошлых уроков
# """Точка входа: демонстрация работы классов и загрузки из JSON."""
#
#
# from pathlib import Path
#
# from src.ecommerce.json_loader import load_categories_from_json
# from src.ecommerce.models import Category, Product
#
# # Корень проекта = папка, где лежит main.py
# BASE_DIR = Path(__file__).resolve().parent
# DATA_FILE = BASE_DIR / "data" / "products.json"
#
#
# def demo() -> None:
#     """Демонстрация функционала."""
#     # Ручное создание объектов
#     p1 = Product("Iphone 15", "512GB, Gray space", 210_000.0, 8)
#     p2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31_000.0, 14)
#     cat = Category("Смартфоны", "Средство коммуникации", [p1, p2])
#
#     print(f"Категория: {cat.name}, товаров в ней: {len(cat.products)}")
#     print(f"Всего категорий: {Category.category_count}")
#     print(f"Всего товаров:   {Category.product_count}")
#
#     # Загрузка из JSON
#     if DATA_FILE.exists():
#         cats = load_categories_from_json(DATA_FILE)
#         print(f"\nЗагружено из JSON категорий: {len(cats)}")
#         for c in cats:
#             print(f" - {c.name}: {len(c.products)} товар(ов)")
#     else:
#         print(f"\nФайл данных не найден: {DATA_FILE}")
#
#
# if __name__ == "__main__":
#     demo()
# from src.ecommerce.models import Product, Category
#
# # Дз 14.2
#
# if __name__ == "__main__":
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3]
#     )
#
#     print(category1.products)
#     product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#     print(category1.product_count)
#
#     new_product = Product.new_product(
#         {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
#          "quantity": 5})
#     print(new_product.name)
#     print(new_product.description)
#     print(new_product.price)
#     print(new_product.quantity)
#
#     new_product.price = 800
#     print(new_product.price)
#
#     new_product.price = -100
#     print(new_product.price)
#     new_product.price = 0
#     print(new_product.price)
from src.ecommerce.models import Product, Category

# Дз 15.1

if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
