from django.urls import path
from . import views

urlpatterns = [
    path('', views.artisans_list_view, name='artisans_list'),
    path('<int:artisan_id>/', views.artisan_detail_view, name='artisan_detail'),
    path('<int:artisan_id>/products/', views.artisan_products_view, name='artisan_products'),
]
