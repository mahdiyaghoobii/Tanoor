from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, full_name, password=None):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password):
        user = self.create_user(phone, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stringPrice = models.CharField(max_length=20)
    quantity = models.IntegerField()
    ingredients = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField()
    comments = models.JSONField(
        default=list,  # پیش‌فرض را یک لیست خالی قرار می‌دهد
        blank=True
    )
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        price = self.price
        if price is not None:
            self.stringPrice = str(price//1000)
        super().save(*args, **kwargs)


class Order(models.Model):
    status_choice = [
        ('Pending', 'در انتظار تایید از سمت تنور'),
        ('Accepted', 'در حال آماده سازی'),
        ('Delivering', 'در حال ارسال'),
        ('Completed', 'انجام شده'),
        ('Cancelled', 'لغو شده'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=status_choice, default='Pending')
    def __str__(self):
        return f"Order {self.id} by {self.user.full_name}"


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    orders = models.ManyToManyField(Order)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت در زمان سفارش

    def __str__(self):
        return f"{self.quantity} x {self.food.name} in Order {self.order.id}"