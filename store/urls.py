from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product/new/", views.ProductCreateView.as_view(), name="product_new"),
    path("product/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("product/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
]