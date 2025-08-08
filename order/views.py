from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({"status": "ok"})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer, OrderDetailSerializer
from .models import Order


class OrderListCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            detail_serializer = OrderDetailSerializer(order)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
