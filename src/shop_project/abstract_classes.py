from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс продукта."""

    def __init__(self, name: str, description: str, price: float, quantity: int, **kwargs):
        if quantity <= 0:
            # Импорт внутри — чтобы не было циклической зависимости
            from .exceptions import ZeroQuantityError
            raise ZeroQuantityError()

        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def __add__(self, other):
        pass


class BaseInfo(ABC):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        pass