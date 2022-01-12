from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_items/', views.updateItem, name='update_items'),
    path('make_payment/', views.submitpaymet, name='make_payment'),
]