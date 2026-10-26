from src.shop_project import LawnGrass, Product


def test_lawn_grass_attributes(grass1):
    assert grass1.country == "Россия"
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"


def test_lawn_grass_is_product_subclass():
    assert issubclass(LawnGrass, Product)


def test_lawn_grass_add(grass1, grass2):
    expected = grass1.price * grass1.quantity + grass2.price * grass2.quantity
    assert grass1 + grass2 == expected
