class Product:
    """Базовый класс товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __add__(self, other):
        """Сложение товаров только одного и того же класса."""
        if type(self) is not type(other):
            raise TypeError(
                "Можно складывать только товары одного класса"
            )
        return self.price * self.quantity + other.price * other.quantity

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.price}, {self.quantity})"
