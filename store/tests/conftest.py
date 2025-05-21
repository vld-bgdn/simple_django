import pytest
from decimal import Decimal
from django.test import Client
from store.models import Category, Product


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def category_data():
    return {"name": "Electronics", "description": "Electronic devices and gadgets"}


@pytest.fixture
def updated_category_data():
    return {"name": "Updated Electronics", "description": "Updated description"}


@pytest.fixture
def product_data():
    return {
        "name": "Smartphone",
        "description": "A modern smartphone",
        "price": Decimal("699.99"),
        "is_published": True,
    }


@pytest.fixture
def updated_product_data():
    return {
        "name": "Updated Smartphone",
        "description": "An updated smartphone",
        "price": Decimal("799.99"),
        "is_published": False,
    }


@pytest.fixture
def validation_data():
    return {
        "short_name": "Test",  # 4 characters - should fail validation
        "valid_name": "Tests",  # 5 characters - should pass validation
        "form_error_name_too_short": "The name must be more than 5 characters",
    }


@pytest.fixture
def new_product_data():
    return {
        "name": "New Test Product",
        "description": "A new test product",
        "price": "199.99",
    }


@pytest.fixture
def category(category_data):
    return Category.objects.create(**category_data)


@pytest.fixture
def second_category():
    return Category.objects.create(name="Appliances")


@pytest.fixture
def product(category, product_data):
    product_dict = product_data.copy()
    product_dict["category"] = category
    return Product.objects.create(**product_dict)


@pytest.fixture
def published_product(category):
    return Product.objects.create(
        name="Published Product",
        description="A published product",
        price=Decimal("99.99"),
        category=category,
        is_published=True,
    )


@pytest.fixture
def unpublished_product(category):
    return Product.objects.create(
        name="Unpublished Product",
        description="An unpublished product",
        price=Decimal("99.99"),
        category=category,
        is_published=False,
    )


@pytest.fixture
def product_form_data(category, product_data):
    form_data = product_data.copy()
    form_data["category"] = category.pk
    return form_data


@pytest.fixture
def new_product_form_data(category, new_product_data):
    form_data = new_product_data.copy()
    form_data["category"] = category.pk
    return form_data


@pytest.fixture
def updated_product_form_data(second_category, updated_product_data):
    form_data = {
        "name": updated_product_data["name"],
        "description": updated_product_data["description"],
        "price": "299.99",
        "category": second_category.pk,
    }
    return form_data
