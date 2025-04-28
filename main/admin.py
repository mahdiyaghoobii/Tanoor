from django.contrib import admin
from rest_framework.views import APIView
from .models import Food, CustomUser,Image
from django.utils.safestring import mark_safe
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Food, Order, OrderItem

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'is_active', 'is_staff', 'is_admin')
    search_fields = ('full_name', 'phone')
    list_filter = ('is_active', 'is_admin', 'is_active')
    ordering = ('-id',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_url', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def image_url(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stringPrice' , 'quantity',
                  'ingredients', 'rating' ,'comments', 'type','created_at', 'image_preview')
    search_fields = ('name','ingredients','rating','comments')
    list_editable = ('price', 'stringPrice', 'quantity')
    list_filter = ('type',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.image.url}" width="50" height="50" />')
        return "No Image"

    image_preview.short_description = 'تصویر'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_food', 'cost', 'status', 'order_date')
    search_fields = ('food__name',)
    list_filter = ('order_date', 'status',)
    ordering = ('-order_date',)

    def get_food(self, obj):
        return ", ".join([item.food.name for item in obj.orderitem.all()])
    get_food.short_description = 'Foods'

    def get_user(self, obj):
        return obj.user.full_name

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#
#     list_display = ('id', 'get_food', 'cost', 'created_at')
#     search_fields = ('food__name',)
#     list_filter = ('created_at',)
#     ordering = ('-created_at',)
#
#     def get_food(self, obj):
#         return ", ".join([Food.name for Food in obj.food.all()])
#     get_food.short_description = 'Foods'
#
#     def get_user(self, obj):
#         return obj.user.full_name

# @admin.register(Food)
# class FoodAdmin(ImportExportModelAdmin):
#     resource_class = FoodResource
#     list_display = ('name', 'price', 'rating', 'type')