from django.urls import path
from . import views

app_name = 'artisanapp'

urlpatterns = [
    path('', views.marketplace_view, name='marketplace'),
]