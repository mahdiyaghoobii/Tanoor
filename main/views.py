from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Food, Order, OrderItem
from .serializer import FoodSerializer, RegisterSerializer, LoginSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import authenticate


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {"phone": user.phone, "full_name": user.full_name},
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # تولید توکن‌ها
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # ذخیره Refresh Token در کوکی HttpOnly
            response = Response({
                "user": {"phone": user.phone, "full_name": user.full_name},
                "access_token": access_token,
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=str(refresh),
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if not refresh_token:
            return Response({"error": "Refresh token not found in cookies."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access_token": access_token,
                "message": "Access token refreshed successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # باطل کردن Refresh Token
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # افزودن به لیست سیاه (نیاز به فعال‌سازی blacklist در تنظیمات)
            # حذف کوکی Refresh Token
            response = Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            return response
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class add_basket(APIView):
    # authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    # permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request, id):
        try:
            food = Food.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"message": "Food is not found."}, status=status.HTTP_404_NOT_FOUND)
        product_data = {
            'id': food.id,
            'name': food.name,
            'price': float(food.price),
            'quantity': 1
        }

        if 'basket' in request.session:
            basket = request.session['basket']
            product_id_str = str(product_data['id'])  # تبدیل id به رشته
            if product_id_str in basket:
                # اگر محصول از قبل در سبد وجود دارد، مقدار quantity را افزایش دهید
                basket[product_id_str]['quantity'] += 1
            else:
                # اگر محصول در سبد وجود ندارد، آن را اضافه کنید
                basket[product_id_str] = product_data

            request.session['basket'] = basket  # ذخیره تغییرات در session
            request.session.modified = True  # اعلام تغییر session به Django
        else:
            # اگر سبد وجود ندارد، یک سبد جدید ایجاد کنید و محصول را اضافه کنید
            product_id_str = str(product_data['id'])  # تبدیل id به رشته
            request.session['basket'] = {product_id_str: product_data}
            request.session.modified = True  # اعلام تغییر session به Django

        cost, basket_items = 0, 0
        for item_key in request.session['basket']:
            item = request.session['basket'][item_key]
            basket_items += item['quantity']
            cost += (item['price']) * int(item['quantity'])

        return Response({"message": f"Product added to basket. {request.session['basket']}", "cost": f"{str(cost)}",
                         "basket_items": f"{str(basket_items)}"}, status=status.HTTP_200_OK)


class decrease_basket(APIView):
    # authentication_classes = []
    # permission_classes = [AllowAny]

    def get(self, request: Request, id):
        if 'basket' in request.session:
            basket = request.session['basket']
            product_id_str = str(id)  # تبدیل id به رشته
            if product_id_str in basket:
                if basket[product_id_str]['quantity'] > 1:
                    # اگر مقدار quantity بیشتر از 1 باشد، آن را کاهش دهید
                    basket[product_id_str]['quantity'] -= 1
                else:
                    # اگر مقدار quantity برابر با 1 باشد، آن را از سبد حذف کنید
                    del basket[product_id_str]

                request.session['basket'] = basket  # ذخیره تغییرات در session
                request.session.modified = True  # اعلام تغییر session به Django

                cost, basket_items = 0, 0
                for item_key in request.session['basket']:
                    item = request.session['basket'][item_key]
                    basket_items += item['quantity']
                    cost += float(item['price']) * int(item['quantity'])

                return Response({"message": f"Product quantity decreased. {request.session['basket']}",
                                 "cost": f"{str(cost)}", "basket_items": f"{str(basket_items)}"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "Product not found in basket."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Basket is empty."}, status=status.HTTP_404_NOT_FOUND)


class clear_basket(APIView):
    # authentication_classes = []
    # permission_classes = [AllowAny]

    def get(self, request):
        if 'basket' in request.session:
            del request.session['basket']  # حذف سبد خرید از session
            request.session.modified = True  # اعلام تغییر session به Django
            return Response({"message": "Basket cleared."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Basket is already empty."},
                            status=status.HTTP_200_OK)  # optional: you can also return 404


class submit_basket(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if 'basket' not in request.session:
            return Response({"message": "Basket is empty."}, status=status.HTTP_404_NOT_FOUND)

        basket = request.session['basket']
        if not basket:
            return Response({"message": "Basket is empty."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # محاسبه هزینه کل و جمع‌آوری اقلام
            order_items = []
            basket_items = 0
            cost = 0

            for item_key in basket:
                item = basket[item_key]
                food = Food.objects.get(id=item['id'])
                quantity = int(item['quantity'])
                price = float(item['price'])
                basket_items += quantity
                cost += price * quantity
                order_items.append({
                    'food': food,
                    'quantity': quantity,
                    'price': price
                })

            # ایجاد سفارش
            order = Order.objects.create(
                user=request.user,
                cost=cost
            )

            # افزودن اقلام به سفارش
            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    food=item['food'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            # پاک کردن سبد خرید
            del request.session['basket']
            request.session.modified = True

            return Response({
                "message": "Basket submitted successfully.",
                "order_id": order.id,
                "cost": str(cost),
                "basket_items": str(basket_items)
            }, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            return Response({"message": "One or more items in the basket are not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FoodListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request: Request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
