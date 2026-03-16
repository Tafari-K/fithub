from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]