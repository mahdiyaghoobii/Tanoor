from django.contrib import admin
from rest_framework.views import APIView
from .models import Food, CustomUser,Image
from django.utils.safestring import mark_safe
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Food
from .resources import FoodResource

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
class FoodAdmin(ImportExportModelAdmin):
    resource_class = FoodResource

    list_display = ('id', 'name', 'price', 'stringPrice' , 'quantity',
                  'ingredients', 'rating' ,'comments', 'type','created_at', 'image_preview')
    search_fields = ('name','ingredients','rating','comments')
    list_filter = ('type',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.image.url}" width="50" height="50" />')
        return "No Image"

    image_preview.short_description = 'تصویر'




# @admin.register(Food)
# class FoodAdmin(ImportExportModelAdmin):
#     resource_class = FoodResource
#     list_display = ('name', 'price', 'rating', 'type')