from django.urls import path
from .views import healthcheck, OrderListCreateAPIView

urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("create-order/", OrderListCreateAPIView.as_view(), name="create_order"),
]
