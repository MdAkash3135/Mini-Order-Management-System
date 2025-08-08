from django.contrib import admin

# Register your models here.
from .models import Customer, Variant, Order, OrderItem

admin.site.register(Customer)
admin.site.register(Variant)
admin.site.register(Order)
admin.site.register(OrderItem)