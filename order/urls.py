from django.urls import path
from .views import healthcheck, OrderListCreateAPIView, CustomerCreateAPIView, VariantListCreateAPIView
from .views import OrderDetailAPIView

urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("create-order/", OrderListCreateAPIView.as_view(), name="create_order"),
    path("create-customer/", CustomerCreateAPIView.as_view(), name="create_customer"),
    path("create-variant/", VariantListCreateAPIView.as_view(), name="variant_list_create"),
    path("order-details/<int:pk>/", OrderDetailAPIView.as_view(), name="order_detail"),

]
