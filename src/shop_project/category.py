from .product import Product


class Category:
    """Категория товаров."""

    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.product_count += len(self.__products)

    @property
    def products(self) -> str:
        """Строковое представление товаров категории."""
        lines = []
        for product in self.__products:
            lines.append(f"{product.name}, {product.price} руб. " f"Остаток: {product.quantity} шт.")
        return "\n".join(lines)

    def add_product(self, product) -> None:
        """Добавить продукт. Принимает только Product и его наследников."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product и его наследников")
        self.__products.append(product)
        Category.product_count += 1

    def __len__(self):
        return len(self.__products)
