from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('',AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menuBuilder/', views.menuBuilder, name='menuBuilder'),
    path('menuBuilder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # category CRUD
    path('menuBuilder/category/add/', views.add_category, name='add_category'),
    path('menuBuilder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menuBuilder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # FoodItem CRUD
    path('menuBuilder/food/add/', views.add_food, name='add_food'),
    path('menuBuilder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menuBuilder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),
]

