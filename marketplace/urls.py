from django.urls import path
from .import views
from .views import vendor_detail


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/',views.vendor_detail, name='vendor_detail'),
]