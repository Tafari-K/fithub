from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product


def product_list(request):
    """
    Display all products
    """
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/product_list.html', context)


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    ordering = ['-created_at']


def product_detail(request, pk):
    """
    Display a single product
    """
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
