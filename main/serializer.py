from rest_framework import serializers
from .models import Food ,Image
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'stringPrice' , 'quantity',
                  'ingredients', 'image', 'rating' ,'comments', 'type','created_at')



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'phone', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data