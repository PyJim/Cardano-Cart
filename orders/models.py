# orders/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('paid', 'Paid')
    ]

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')  # Buyer is a user

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')  # Single product per order

    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    order_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Calculated as product.price * quantity

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} - {self.status}"

    def save(self, *args, **kwargs):
        """Override save method to automatically calculate total_amount."""
        self.total_amount = self.product.price * self.quantity
        super(Order, self).save(*args, **kwargs)
