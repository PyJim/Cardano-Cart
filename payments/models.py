from django.db import models
from django.utils import timezone

from orders.models import Order  # Replace 'orders' with the actual app name

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('crypto', 'Crypto'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='crypto')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - {self.payment_status}"
