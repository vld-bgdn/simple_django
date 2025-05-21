import pytest
from store.forms import ProductForm
from decimal import Decimal


@pytest.mark.django_db
class TestProductForm:
    def test_valid_form(self, product_form_data):
        """Test that form accepts valid data"""
        form = ProductForm(data=product_form_data)
        assert form.is_valid()

    def test_name_validation(self, product_form_data, validation_data):
        """Test the name field validation (minimum 5 characters)"""
        form_data = product_form_data.copy()
        form_data["name"] = validation_data["short_name"]

        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert "name" in form.errors
        assert form.errors["name"][0] == validation_data["form_error_name_too_short"]

        form_data["name"] = validation_data["valid_name"]
        form = ProductForm(data=form_data)
        assert form.is_valid()

    def test_empty_description(self, product_form_data):
        """Test that an empty description is valid (it's allowed to be blank)"""
        form_data = product_form_data.copy()
        form_data["description"] = ""

        form = ProductForm(data=form_data)
        assert form.is_valid()

    def test_negative_price(self, product_form_data):
        """Test that negative price is rejected (Django's DecimalField validation)"""
        form_data = product_form_data.copy()
        form_data["price"] = Decimal("-99.99")

        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert "price" in form.errors

    def test_missing_required_fields(self):
        """Test that missing required fields cause validation errors"""
        form_data = {"description": "This is a test product"}
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert "name" in form.errors
        assert "price" in form.errors
        assert "category" in form.errors
