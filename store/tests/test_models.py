# store/tests/test_models.py
import pytest
from store.models import Product, Category

@pytest.mark.django_db
def test_create_product():
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        name="Test Product",
        categories=category,
        alcohol=5.0,
        color="Red",
        amargor="Medio",
        descripcion="A test product description",
        price=19.99,
        casa="Test House",
        stock=50,
        image="uploads/product/test_image.jpg",
        is_sale=True,
        sale_price=14.99
    )
    assert product.name == "Test Product"
    assert product.categories == category
    assert product.alcohol == 5.0
    assert product.color == "Red"
    assert product.amargor == "Medio"
    assert product.descripcion == "A test product description"
    assert product.price == 19.99  # Corrige esta línea
    assert product.casa == "Test House"
    assert product.stock == 50
    assert str(product.image) == "uploads/product/test_image.jpg"
    assert product.is_sale is True
    assert product.sale_price == 14.99
