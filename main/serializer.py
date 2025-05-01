from rest_framework import serializers
from .models import Food, Image, Order, OrderItem
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
        fields = ('id', 'name', 'price', 'stringPrice', 'quantity',
                  'ingredients', 'image', 'rating', 'comments', 'type', 'created_at')




class OrderItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True) # Use nested FoodSerializer for read operations
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), source='food', write_only=True) # Use PrimaryKeyRelatedField for write operations
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True) # Keep order as write_only if it's not needed in the item representation

    class Meta:
        model = OrderItem
        # Include 'food' for nested details and 'food_id' for writing.
        # 'order' is typically not included in the item representation itself.
        fields = ('id', 'quantity', 'price', 'food', 'food_id', 'order')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) # Represents the user ID
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set') # Nested serializer for order items

    class Meta:
        model = Order
        fields = ('id', 'user', 'cost', 'status', 'order_date', 'items') # Add 'items' field


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['phone', 'full_name', 'password']

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials or inactive account.")
