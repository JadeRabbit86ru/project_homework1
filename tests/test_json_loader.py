import json

from src.ecommerce.json_loader import load_categories_from_json
from src.ecommerce.models import Category
from src.ecommerce.models import Product

"""Тесты загрузки данных из JSON."""


def test_load_from_json(tmp_path):
    data = [
        {
            "name": "Телевизоры",
            "description": "desc",
            "products": [
                {
                    "name": '55" QLED 4K',
                    "description": "Фоновая подсветка",
                    "price": 123000.0,
                    "quantity": 7,
                }
            ],
        }
    ]
    f = tmp_path / "products.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    cats = load_categories_from_json(f)

    assert len(cats) == 1
    assert isinstance(cats[0], Category)
    assert cats[0].name == "Телевизоры"
    assert len(cats[0].products) == 1
    assert isinstance(cats[0].products[0], Product)
    assert cats[0].products[0].price == 123000.0
    assert cats[0].products[0].quantity == 7


def test_load_from_real_data_file():
    """Опционально: проверка, что реальный data/products.json парсится."""
    from pathlib import Path

    real = Path(__file__).resolve().parent.parent / "data" / "products.json"
    if not real.exists():
        import pytest

        pytest.skip("data/products.json отсутствует")

    cats = load_categories_from_json(real)
    assert len(cats) == 2
    assert cats[0].name == "Смартфоны"
    assert len(cats[0].products) == 3
    assert cats[1].name == "Телевизоры"
