from django.urls import path
from .views import ProductView

urlpatterns = [
    path('', ProductView.as_view(), name='product-list-create'),
    path('<int:id>/', ProductView.as_view(), name='get-update-delete-product'),
]