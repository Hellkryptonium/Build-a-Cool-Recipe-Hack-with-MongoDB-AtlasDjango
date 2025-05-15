from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<str:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<str:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<str:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<str:pk>/recommendations/', views.get_recommendations, name='get_recommendations'),
]
