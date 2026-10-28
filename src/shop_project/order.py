from .abstract_classes import BaseInfo
from .product import Product


class Order(BaseInfo):
    """Заказ — один товар + количество + итоговая стоимость (доп. задание)."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("В заказ можно добавить только Product и его наследников")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")

        super().__init__(product.name, f"Заказ на {product.name}")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    @property
    def __str__(self) -> str:
        return (
            f"Заказ: {self.product.name}, количество: {self.quantity}, "
            f"итого: {self.total_price} руб."
        )
