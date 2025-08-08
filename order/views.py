from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


from rest_framework import generics
from .models import Customer, Variant
from .serializers import *


def healthcheck(request):
    return JsonResponse({"status": "ok"})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

from .tasks import process_order


class OrderCreateAPIView(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        items = request.data.get("items", [])

        if not customer_id or not items:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        process_order.delay(customer_id, items)  # queue task

        return Response({"message": "Order is being processed"}, status=status.HTTP_202_ACCEPTED)


class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer

class VariantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer



class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer



class CustomerReportAPIView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerReportSerializer