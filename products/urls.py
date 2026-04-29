from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    add_product,
    edit_product,
    delete_product,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('add/', add_product, name='add_product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', edit_product, name='edit_product'),
    path('<int:pk>/delete/', delete_product, name='delete_product'),
]