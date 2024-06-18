from django.contrib import admin
from .models import Order, Invoice, cart, OrderAmount, cart_records, customerOrderHistory

# Register your models here.
admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(cart)
admin.site.register(OrderAmount)
admin.site.register(cart_records)
admin.site.register(customerOrderHistory)
