from .product import Product


class Smartphone(Product):
    """Смартфон — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self):
        return (
            f"Smartphone({self.name!r}, model={self.model!r}, "
            f"memory={self.memory}, color={self.color!r})"
        )
