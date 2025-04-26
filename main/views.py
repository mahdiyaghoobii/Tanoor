from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from .models import Food
from .serializer import FoodSerializer, RegisterSerializer, LoginSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class FoodListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request:Request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class add_basket(APIView):
    authentication_classes = []  # غیرفعال کردن JWT برای این ویو
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request: Request, id):
        try:
            food = Food.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"message": "Food is not found."}, status=status.HTTP_404_NOT_FOUND)
        product_data = {
            'id': food.id,
            'name': food.name,
            'price': str(food.price),
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
            cost += float(item['price']) * int(item['quantity'])

        return Response({"message": f"Product added to basket. {request.session['basket']}", "cost": f"{str(cost)}",
                         "basket_items": f"{str(basket_items)}"}, status=status.HTTP_200_OK)

class decrease_basket(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

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
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        if 'basket' in request.session:
            del request.session['basket']  # حذف سبد خرید از session
            request.session.modified = True  # اعلام تغییر session به Django
            return Response({"message": "Basket cleared."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Basket is already empty."},
                            status=status.HTTP_200_OK)  # optional: you can also return 404
