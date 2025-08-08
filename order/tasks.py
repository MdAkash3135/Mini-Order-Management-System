from celery import shared_task
from django.db import transaction
from .models import Order, OrderItem, Customer, Variant

@shared_task
def process_order(customer_id, items_data):
    customer = Customer.objects.get(id=customer_id)

    with transaction.atomic():
        order = Order.objects.create(customer=customer)

        order_items = []
        total_amount = 0

        for item in items_data:
            variant = Variant.objects.get(id=item['variant_id'])

            if item['price'] < variant.cost_price:
                raise ValueError(f"Price for variant {variant.name} below cost price.")

            order_items.append(OrderItem(
                order=order,
                variant=variant,
                quantity=item['quantity'],
                price=item['price']
            ))

            total_amount += item['price'] * item['quantity']

        OrderItem.objects.bulk_create(order_items)

        # Update customer total spent
        customer.total_spent += total_amount
        customer.save()

    return f"Order {order.id} processed for customer {customer.name}"
