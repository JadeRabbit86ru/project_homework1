class ReprMixin:
    """Миксин: печатает информацию о созданном объекте в консоль."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        values = ", ".join(repr(value) for value in self.__dict__.values())
        return f"{self.__class__.__name__}({values})"
