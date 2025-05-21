import pytest
from django.urls import reverse
from store.models import Product
from decimal import Decimal


@pytest.mark.django_db
class TestProductListView:
    def setup_method(self):
        self.url = reverse("store:product_list")

    def test_view_url_exists(self, client):
        """Test that the URL exists"""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Test that the view uses the correct template"""
        response = client.get(self.url)
        assert "store/product_list.html" in [t.name for t in response.templates]

    def test_shows_only_published_products(
        self, client, published_product, unpublished_product
    ):
        """Test that only published products are shown"""
        response = client.get(self.url)
        assert "Published Product" in response.content.decode()
        assert "Unpublished Product" not in response.content.decode()


@pytest.mark.django_db
class TestProductDetailView:
    @pytest.fixture(autouse=True)
    def setup_method(self, product):
        self.product = product
        self.url = reverse("store:product_detail", kwargs={"pk": self.product.pk})

    def test_view_url_exists(self, client):
        """Test that the URL exists"""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Test that the view uses the correct template"""
        response = client.get(self.url)
        assert "store/product_detail.html" in [t.name for t in response.templates]

    def test_shows_product_details(self, client, product, product_data, category_data):
        """Test that product details are displayed correctly"""
        response = client.get(self.url)
        content = response.content.decode()

        assert product_data["name"] in content
        assert product_data["description"] in content
        assert str(product_data["price"]).rstrip("0").rstrip(".") in content
        assert category_data["name"] in content


@pytest.mark.django_db
class TestProductCreateView:
    def setup_method(self):
        self.url = reverse("store:product_new")

    def test_view_url_exists(self, client):
        """Test that the URL exists"""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Test that the view uses the correct template"""
        response = client.get(self.url)
        assert "store/product_form.html" in [t.name for t in response.templates]

    def test_context_has_title(self, client):
        """Test that the context contains the expected title"""
        response = client.get(self.url)
        assert response.context["title"] == "Add New Product"

    def test_form_submission(self, client, new_product_form_data, new_product_data):
        """Test successful form submission"""
        response = client.post(self.url, new_product_form_data)

        assert Product.objects.count() == 1
        new_product = Product.objects.first()

        assert response.status_code == 302
        assert response.url == reverse(
            "store:product_detail", kwargs={"pk": new_product.pk}
        )
        assert new_product.name == new_product_data["name"]
        assert new_product.description == new_product_data["description"]
        assert new_product.price == Decimal(new_product_data["price"])


@pytest.mark.django_db
class TestProductUpdateView:
    @pytest.fixture(autouse=True)
    def setup_method(self, product):
        self.product = product
        self.url = reverse("store:product_edit", kwargs={"pk": self.product.pk})

    def test_view_url_exists(self, client):
        """Test that the URL exists"""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Test that the view uses the correct template"""
        response = client.get(self.url)
        assert "store/product_form.html" in [t.name for t in response.templates]

    def test_context_has_title(self, client):
        """Test that the context contains the expected title"""
        response = client.get(self.url)
        assert response.context["title"] == "Edit Product"

    def test_form_submission(
        self,
        client,
        product,
        updated_product_form_data,
        updated_product_data,
        second_category,
    ):
        """Test successful form submission"""
        response = client.post(self.url, updated_product_form_data)
        product.refresh_from_db()

        assert response.status_code == 302
        assert response.url == reverse(
            "store:product_detail", kwargs={"pk": product.pk}
        )
        assert product.name == updated_product_data["name"]
        assert product.description == updated_product_data["description"]
        assert product.price == Decimal("299.99")
        assert product.category == second_category

    def test_invalid_form_submission(self, client, product, category, validation_data):
        """Test invalid form submission (name too short)"""
        form_data = {
            "name": validation_data["short_name"],  # Too short
            "description": "An updated test product",
            "price": "299.99",
            "category": category.pk,
        }

        response = client.post(self.url, form_data)
        product.refresh_from_db()

        assert response.status_code == 200
        assert "form" in response.context
        form = response.context["form"]
        assert not form.is_valid()
        assert "name" in form.errors
        assert form.errors["name"][0] == validation_data["form_error_name_too_short"]
        assert product.name == "Smartphone"


@pytest.mark.django_db
class TestProductDeleteView:
    @pytest.fixture(autouse=True)
    def setup_method(self, product):
        self.product = product
        self.url = reverse("store:product_delete", kwargs={"pk": self.product.pk})
        self.redirect_url = reverse("store:product_list")

    def test_view_url_exists(self, client):
        """Test that the URL exists"""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Test that the view uses the correct template"""
        response = client.get(self.url)
        assert "store/product_confirm_delete.html" in [
            t.name for t in response.templates
        ]

    def test_delete_product(self, client):
        """Test that a product can be deleted through the view"""
        response = client.post(self.url)

        assert response.status_code == 302
        assert response.url == self.redirect_url
