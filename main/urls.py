from django.urls import path, include
from .views import FoodListView
urlpatterns = [
    path('foods/', views.FoodListView.as_view(), name='foods-list'),
]
