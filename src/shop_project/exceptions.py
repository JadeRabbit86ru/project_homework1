class ZeroQuantityError(ValueError):
    """Исключение: попытка добавить/создать товар с нулевым количеством."""

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен"):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
