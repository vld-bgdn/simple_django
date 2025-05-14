from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("product/new/", views.product_new, name="product_new"),
    path("product/<int:pk>/edit/", views.product_edit, name="product_edit"),
]
