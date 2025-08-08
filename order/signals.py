from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem


def update_customer_total_spent(customer):
    total = 0
    for order in customer.orders.all():
        total += order.total_amount
    customer.total_spent = total
    customer.save(update_fields=["total_spent"])


@receiver([post_save, post_delete], sender=OrderItem)
def recalculate_total_spent(sender, instance, **kwargs):
    update_customer_total_spent(instance.order.customer)
