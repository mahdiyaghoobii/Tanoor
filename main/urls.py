from django.urls import path, include
from . import views
urlpatterns = [
    path('foods/', views.FoodListView.as_view(), name='foods-list'),
]
