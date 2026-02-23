from django.urls import path
from .views import ProductListView, ProductDetailView, ReviewCreateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),

]
