from src.shop_project import LawnGrass, Product, Smartphone


def test_product_prints_repr_on_init(capsys):
    Product("Продукт1", "Описание продукта", 1200, 10)
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "Продукт1" in captured.out
    assert "Описание продукта" in captured.out
    assert "1200" in captured.out


def test_smartphone_prints_repr_with_extras(capsys):
    Smartphone("Phone", "Desc", 1000.0, 2, 90.0, "X", 128, "Black")
    out = capsys.readouterr().out
    assert "Smartphone(" in out
    assert "Phone" in out
    assert "90.0" in out
    assert "128" in out
    assert "Black" in out


def test_lawn_grass_prints_repr(capsys):
    LawnGrass("Трава", "Desc", 100.0, 5, "RU", "3 дня", "Green")
    out = capsys.readouterr().out
    assert "LawnGrass(" in out
    assert "RU" in out
    assert "3 дня" in out


def test_repr_format(product):
    assert repr(product) == "Product('Товар', 'Описание', 100.0, 10)"
