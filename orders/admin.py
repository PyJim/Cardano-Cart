from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_amount', 'status', 'order_date', 'created_at', 'updated_at')
    search_fields = ('buyer__username', 'tracking_number')
    list_filter = ('status', 'order_date', 'created_at')
