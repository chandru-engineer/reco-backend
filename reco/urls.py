from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ActiveProductsView.as_view(), name='active-product'),
]
