from django.shortcuts import render
from rest_framework.views import APIView
from .models import Food
# Create your views here.


class FoodListView(APIView):
    """
    API view to retrieve list of foods.
    """
    def get(self, request, *args, **kwargs):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)