from django.contrib import admin
from rest_framework.views import APIView
from .models import Food, CustomUser
from django.utils.safestring import mark_safe


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'is_active', 'is_staff', 'is_admin')
    search_fields = ('full_name', 'phone')
    list_filter = ('is_active', 'is_admin', 'is_active')
    ordering = ('-id',)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stringPrice' , 'quantity',
                  'ingredients', 'rating' ,'comments', 'type','created_at', 'image_preview')
    search_fields = ('name','ingredients','rating','comments')
    list_filter = ('type',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.image_url.url}" width="50" height="50" />')
        return "No Image"

    image_preview.short_description = 'تصویر'