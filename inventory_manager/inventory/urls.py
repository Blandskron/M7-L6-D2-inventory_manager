from django.urls import path
from . import views

urlpatterns = [

    # PRODUCTOS
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/edit/<int:id>/', views.product_update, name='product_update'),
    path('products/delete/<int:id>/', views.product_delete, name='product_delete'),

    # MOVIMIENTOS
    path('movements/', views.movement_list, name='movement_list'),
    path('movements/create/', views.movement_create, name='movement_create'),
    path('movements/delete/<int:id>/', views.movement_delete, name='movement_delete'),
]