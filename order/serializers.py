from rest_framework import serializers
from .models import Customer, Variant, Order, OrderItem


class OrderItemSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def validate(self, data):
        variant_id = data.get("variant_id")
        price = data.get("price")

        try:
            variant = Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            raise serializers.ValidationError(f"Variant with id {variant_id} does not exist.")

        if price < variant.cost_price:
            raise serializers.ValidationError(
                f"Price {price} is below cost price {variant.cost_price} for variant '{variant.name}'."
            )

        return data


class OrderCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)

    def validate_customer_id(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer does not exist.")
        return value

    def create(self, validated_data):
        customer_id = validated_data["customer_id"]
        items_data = validated_data["items"]

        customer = Customer.objects.get(id=customer_id)
        order = Order.objects.create(customer=customer)

        for item_data in items_data:
            variant = Variant.objects.get(id=item_data["variant_id"])
            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=item_data["quantity"],
                price=item_data["price"],
            )
        return order


class OrderItemDetailSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.name", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "variant_name", "quantity", "price", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    items = OrderItemDetailSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_name", "created_at", "items", "total_amount"]
