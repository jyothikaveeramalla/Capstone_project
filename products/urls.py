from django.urls import path
from . import views
from .product_management import (
    add_product_view, edit_product_view, delete_product_view, my_products_view
)

urlpatterns = [
    # Public product views
    path('', views.products_list_view, name='products_list'),
    path('<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('<int:product_id>/review/', views.add_review_view, name='add_review'),
    
    # Artisan-only product management
    path('manage/my/', my_products_view, name='my_products'),
    path('manage/add/', add_product_view, name='add_product'),
    path('manage/<int:product_id>/edit/', edit_product_view, name='edit_product'),
    path('manage/<int:product_id>/delete/', delete_product_view, name='delete_product'),
]
