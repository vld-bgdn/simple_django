from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Product
from .forms import ProductForm
from .tasks import log_new_product_task


class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            log_new_product_task.delay(
                product_name=self.object.name,
                product_id=self.object.id,
                category_name=self.object.category.name,
                price=str(self.object.price),
            )
        except Exception as e:
            print(f"Failed to queue Celery task: {e}")

        return response

    def get_success_url(self):
        return reverse_lazy("store:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Product"
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def get_success_url(self):
        return reverse_lazy("store:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Product"
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "store/product_confirm_delete.html"
    success_url = reverse_lazy("store:product_list")
    context_object_name = "product"
