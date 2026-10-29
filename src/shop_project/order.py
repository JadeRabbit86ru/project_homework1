from .abstract_classes import BaseInfo
from .exceptions import ZeroQuantityError
from .product import Product


class Order(BaseInfo):
    """Заказ — один товар + количество + итоговая стоимость (доп. задание)."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("В заказ можно добавить только Product и его наследников")

        try:
            if quantity <= 0:
                raise ZeroQuantityError()
            if quantity > product.quantity:
                raise ValueError("Недостаточно товара на складе")
        except ZeroQuantityError:
            print("Не удалось добавить товар: количество равно нулю")
            raise
        else:
            print(f"Товар {product.name} успешно добавлен в заказ")
        finally:
            print("Обработка добавления товара завершена")

        super().__init__(product.name, f"Заказ на {product.name}")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self) -> str:
        return (
            f"Заказ: {self.product.name}, количество: {self.quantity}, "
            f"итого: {self.total_price} руб."
        )
