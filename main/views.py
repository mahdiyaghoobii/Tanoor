from django.shortcuts import render
from rest_framework import status
from rest_framework.status import HTTP_207_MULTI_STATUS
from rest_framework.views import APIView
from .models import Food
from .serializer import FoodSerializer
from rest_framework.request import Request
from rest_framework.response import Response

# Create your views here.


class FoodListView(APIView):
    def get(self, request:Request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)