import json
from pathlib import Path
from typing import List, Union

from .models import Category, Product

"""Загрузка категорий и товаров из JSON-файла."""


def load_categories_from_json(path: Union[str, Path]) -> List[Category]:
    """Читает JSON и возвращает список объектов Category с Product внутри."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    categories: List[Category] = []
    for cat in raw:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=float(p["price"]),
                quantity=int(p["quantity"]),
            )
            for p in cat.get("products", [])
        ]
        categories.append(
            Category(
                name=cat["name"],
                description=cat["description"],
                products=products,
            )
        )
    return categories
