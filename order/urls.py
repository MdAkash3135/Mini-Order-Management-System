from django.urls import path
from .views import healthcheck, OrderListCreateAPIView, CustomerCreateAPIView

urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("create-order/", OrderListCreateAPIView.as_view(), name="create_order"),
    path("create-customer/", CustomerCreateAPIView.as_view(), name="create_customer"),
]
