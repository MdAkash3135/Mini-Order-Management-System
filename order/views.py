from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({"status": "ok"})