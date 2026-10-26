from .product import Product


class LawnGrass(Product):
    """Газонная трава — наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self):
        return (
            f"LawnGrass({self.name!r}, country={self.country!r}, "
            f"germination_period={self.germination_period!r}, color={self.color!r})"
        )
