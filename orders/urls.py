from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list_view, name='orders_list'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('<int:order_id>/', views.order_detail_view, name='order_detail'),
]
