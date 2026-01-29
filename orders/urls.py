from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list_view, name='orders_list'),
    path('<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirm/', views.order_confirm_view, name='order_confirm'),
]
