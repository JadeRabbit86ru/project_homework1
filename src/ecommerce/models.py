from typing import List

"""Модели предметной области интернет-магазина."""


class Product:
    """Товар интернет-магазина."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Категория товаров. Хранит общую статистику по всем категориям."""

    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    products: List[Product]

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        self.name = name
        self.description = description
        self.products = products

        # Атрибуты класса заполняются автоматически при инициализации
        Category.category_count += 1
        Category.product_count += len(products)
