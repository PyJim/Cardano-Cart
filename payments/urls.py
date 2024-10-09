from django.urls import path
from .views import GetPaymentAddressView, VerifyPaymentView

urlpatterns = [
    path('get_address/<int:product_id>/', GetPaymentAddressView.as_view(), name='get_address'),
    path('verify_payment/<int:order_id>/', VerifyPaymentView.as_view(), name='verify_payment')
]
