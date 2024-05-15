# store/tests/test_product_methods.py
import pytest
from store.models import Product, Category

@pytest.mark.django_db
def test_get_discounted_price():
    category = Category.objects.create(name="Test Category")
    
    # Producto sin descuento
    product = Product.objects.create(
        name="Product 1",
        categories=category,
        alcohol=5.0,
        color="Red",
        amargor="Medio",
        descripcion="Description 1",
        price=100.00,
        casa="House 1",
        stock=50,
        image="uploads/product/test1.jpg",
        is_sale=False,
        sale_price=80.00
    )
    assert product.get_discounted_price() == 100.00

    # Producto con descuento
    product.is_sale = True
    product.save()
    assert product.get_discounted_price() == 80.00
