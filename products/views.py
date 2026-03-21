from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


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

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.GET.get('category')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category__slug=category)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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