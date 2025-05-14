from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "product_count")
    search_fields = ("name",)

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Number of Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "created_at", "is_published")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"

    @admin.action(description="Apply 10 perscent discount")
    def apply_discount(self, request, queryset):
        for product in queryset:
            price_as_int = int(product.price)
            discounted_price = price_as_int * 9 // 10
            product.price = discounted_price
            product.save()

    @admin.action(description="Mark selected products as published")
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} products were marked as published.")

    @admin.action(description="Mark selected products as unpublished")
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} products were marked as unpublished.")

    actions = [apply_discount, make_published, make_unpublished]
