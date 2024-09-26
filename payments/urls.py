from django.urls import path
from .views import GeneratePaymentAddressView

urlpatterns = [
    path('generate-address/', GeneratePaymentAddressView.as_view(), name='generate_address'),
]
