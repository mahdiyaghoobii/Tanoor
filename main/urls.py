from django.urls import path, include
from . import views


urlpatterns = [
    path('foods/', views.FoodListView.as_view(), name='foods-list'),
    path('add-to-basket/<int:id>/', views.add_basket.as_view(), name='add_to_basket'),
    path('decrease_basket/<int:id>/', views.decrease_basket.as_view(), name='decrease_basket'),
    path('clear_basket/', views.clear_basket.as_view(), name='clear_basket'),
    path('submit_basket/', views.submit_basket.as_view(), name='submit_basket'),

]
