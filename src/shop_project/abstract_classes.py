from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс продукта.

    Описывает общую для всех продуктов функциональность:
    name, description, price, quantity и абстрактный __add__.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int, **kwargs):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        # Дополнительные атрибуты наследников (efficiency, model, ...)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def __add__(self, other):
        """Сложение товаров одного класса."""
        pass


class BaseInfo(ABC):
    """Абстрактный класс с общей информацией для Category и Order."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление объекта."""
        pass
