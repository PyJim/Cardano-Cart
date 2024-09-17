# cart/urls.py
from django.urls import path
from .views import CartProductView

urlpatterns = [
    path('', CartProductView.as_view(), name='product_to_cart'),
    path('<int:product_id>/', CartProductView.as_view(), name='product_in_cart'),
]
