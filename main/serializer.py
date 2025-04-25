from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'stringPrice' , 'quantity',
                  'ingredients', 'image', 'rating' ,'comments', 'type','created_at')