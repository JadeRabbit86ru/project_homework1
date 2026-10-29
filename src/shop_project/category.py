"""Предыдущая работа"""
# from .product import Product
#
#
# class Category:
#     """Категория товаров."""
#
#     product_count = 0
#
#     def __init__(self, name: str, description: str, products: list):
#         self.name = name
#         self.description = description
#         self.__products = list(products)
#         Category.product_count += len(self.__products)
#
#     @property
#     def products(self) -> str:
#         """Строковое представление товаров категории."""
#         lines = []
#         for product in self.__products:
#             lines.append(f"{product.name}, {product.price} руб. " f"Остаток: {product.quantity} шт.")
#         return "\n".join(lines)
#
#     def add_product(self, product) -> None:
#         """Добавить продукт. Принимает только Product и его наследников."""
#         if not isinstance(product, Product):
#             raise TypeError("В категорию можно добавлять только объекты Product и его наследников")
#         self.__products.append(product)
#         Category.product_count += 1
#
#     def __len__(self):
#         return len(self.__products)

"""Работа 16.2 и 17.1"""

from .abstract_classes import BaseInfo
from .product import Product


class Category(BaseInfo):
    """Категория товаров — наследник BaseInfo."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        super().__init__(name, description)
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    @property
    def products(self) -> list:
        return self.__products

    def add_product(self, product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты Product и его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    def average_price(self) -> float:
        """Средняя цена товаров в категории.

        Возвращает 0, если товаров нет (обработка ZeroDivisionError).
        """
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0

    def __str__(self) -> str:
        lines = []
        for product in self.__products:
            lines.append(
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт."
            )
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self.__products)

    def __len__(self) -> int:
        return len(self.__products)
