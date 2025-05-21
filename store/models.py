from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name
