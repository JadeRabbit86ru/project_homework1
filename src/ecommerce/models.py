# from typing import List

# """Модели предметной области интернет-магазина."""
#
#
# class Product:
#     """Товар интернет-магазина."""
#
#     name: str
#     description: str
#     price: float
#     quantity: int
#
#     def __init__(
#             self,
#             name: str,
#             description: str,
#             price: float,
#             quantity: int,
#     ) -> None:
#         self.name = name
#         self.description = description
#         self.price = price
#         self.quantity = quantity
#
#
# class Category:
#     """Категория товаров. Хранит общую статистику по всем категориям."""
#
#     category_count: int = 0
#     product_count: int = 0
#
#     name: str
#     description: str
#     products: List[Product]
#
#     def __init__(
#             self,
#             name: str,
#             description: str,
#             products: List[Product],
#     ) -> None:
#         self.name = name
#         self.description = description
#         self.products = products
#
#         # Атрибуты класса заполняются автоматически при инициализации
#         Category.category_count += 1
#         Category.product_count += len(products)


# """Работа 14.2"""
#
#
# class Product:
#     def __init__(self, name: str, description: str, price: float, quantity: int):
#         self.name = name
#         self.description = description
#         self.__price = price  # Приватный атрибут цены
#         self.quantity = quantity
#
#     @property
#     def price(self):
#         """Геттер для цены"""
#         return self.__price
#
#     @price.setter
#     def price(self, new_price: float):
#         """Сеттер с проверкой на положительное значение"""
#         if new_price <= 0:
#             print("Цена не должна быть нулевая или отрицательная")
#             return
#
#         # Доп. задание: подтверждение понижения цены
#         if new_price < self.__price:
#             answer = input(f"Понизить цену с {self.__price} до {new_price}? (y/n): ")
#             if answer.lower() != "y":
#                 return
#
#         self.__price = new_price
#
#     @classmethod
#     def new_product(cls, product_data: dict, products_list: list = None):
#         """
#         Класс-метод для создания товара из словаря.
#         Если передан список товаров, ищет дубликаты по имени.
#         """
#         name = product_data.get("name")
#         description = product_data.get("description")
#         price = product_data.get("price")
#         quantity = product_data.get("quantity")
#
#         if products_list is not None:
#             for existing_product in products_list:
#                 if existing_product.name == name:
#                     # Складываем количество
#                     existing_product.quantity += quantity
#                     # Выбираем наибольшую цену
#                     if price > existing_product.price:
#                         existing_product.price = price
#                     return existing_product
#
#         # Если дубликат не найден, создаем новый объект
#         return cls(name, description, price, quantity)
#
#
# class Category:
#     category_count = 0
#     product_count = 0
#
#     def __init__(self, name: str, description: str, products: list = None):
#         self.name = name
#         self.description = description
#         # Приватный атрибут списка товаров
#         self.__products = products if products is not None else []
#
#         # Увеличиваем счетчики при инициализации
#         Category.category_count += 1
#         Category.product_count += len(self.__products)
#
#     def add_product(self, product: Product):
#         """Добавляет продукт в категорию"""
#         self.__products.append(product)
#         Category.product_count += 1
#
#     @property
#     def products(self):
#         """Геттер, возвращающий строку со списком товаров"""
#         result = ""
#         for product in self.__products:
#             result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
#         return result

"""Работ 15.1"""


class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, Product):
            return (self.price * self.quantity) + (other.price * other.quantity)
        return NotImplemented


class Category:
    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

    @property
    def products(self):
        return self.__products

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
