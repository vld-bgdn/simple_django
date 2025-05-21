import pytest
from store.models import Category, Product


@pytest.mark.django_db
class TestCategoryModel:
    def test_category_creation(self, category, category_data):
        """Test that a category can be created"""
        assert category.name == category_data["name"]
        assert category.description == category_data["description"]

    def test_category_update(self, category, updated_category_data):
        """Test that a category can be updated"""
        category.name = updated_category_data["name"]
        category.description = updated_category_data["description"]
        category.save()

        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == updated_category_data["name"]
        assert updated_category.description == updated_category_data["description"]


@pytest.mark.django_db
class TestProductModel:
    def test_product_creation(self, product, product_data, category):
        """Test that a product can be created"""
        assert product.name == product_data["name"]
        assert product.description == product_data["description"]
        assert product.price == product_data["price"]
        assert product.category == category
        assert product.is_published is product_data["is_published"]

    def test_product_update(self, product, updated_product_data):
        """Test that a product can be updated"""
        product.name = updated_product_data["name"]
        product.description = updated_product_data["description"]
        product.price = updated_product_data["price"]
        product.is_published = updated_product_data["is_published"]
        product.save()

        updated_product = Product.objects.get(id=product.id)
        assert updated_product.name == updated_product_data["name"]
        assert updated_product.description == updated_product_data["description"]
        assert updated_product.price == updated_product_data["price"]
        assert updated_product.is_published is updated_product_data["is_published"]

    def test_product_deletion(self, product):
        """Test that a product can be deleted"""
        product_id = product.id
        product.delete()

        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(id=product_id)
