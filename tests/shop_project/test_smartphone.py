from src.shop_project import Smartphone


def test_smartphone_attributes(smartphone1):
    assert smartphone1.name == "Samsung Galaxy S23 Ultra"
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"


def test_smartphone_is_product_subclass():
    from src.shop_project import Product
    assert issubclass(Smartphone, Product)


def test_smartphone_add(smartphone1, smartphone2):
    expected = (
        smartphone1.price * smartphone1.quantity
        + smartphone2.price * smartphone2.quantity
    )
    assert smartphone1 + smartphone2 == expected
