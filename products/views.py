from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from products.forms import ReviewForm
from .models import Product, Review, Category
from django.db.models import Avg, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


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
            queryset = queryset.filter(category_slug=category)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            has_reviewed = Review.objects.filter(
                product=self.object,
                user=self.request.user
            ).exists()
        else:
            has_reviewed = False

        context['has_reviewed'] = has_reviewed
        context['form'] = ReviewForm()
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form.instance.product = product
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.kwargs['pk']})


@property
def average_rating(self):
    return self.reviews.aggregate(avg=Avg('rating'))['avg']