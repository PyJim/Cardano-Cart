from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'amount', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('order__id', 'payment_status')

admin.site.register(Payment, PaymentAdmin)
