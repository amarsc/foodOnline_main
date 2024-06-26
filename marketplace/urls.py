from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews

urlpatterns = [
    path('',views.marketplace, name='marketplace'),
    #Cart
    path('cart/',views.cart, name='cart'),
    path('<slug:vendor_slug>/',views.vendor_detail, name='vendor_detail'),
    
    
    # add to cart
    path('add_to_cart/<int:food_id>/',views.add_to_cart, name='add_to_cart'),

    # decrease cart
    path('decrease_cart/<int:food_id>/',views.decrease_cart, name='decrease_cart'),
    
    #delete cart
    path('delete_cart/<int:cart_id>/',views.delete_cart, name='delete_cart'),
   
]