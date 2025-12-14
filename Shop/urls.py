from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/',Register,name='register'),
    path('login/',LoginPage,name='login'),
    path('accounts/logout/',LogoutPage,name='logout'),
    path('collection',Collections,name='collection'),
    path('collectionview/<str:name>/',CollectionsView,name='collectionview'),
    path('Productsdetails/<str:cname>/<str:pname>/',ProductDetails,name='productdetails'),

# carts
  path('add_to_cart/<int:id>/',AddToCart,name='add_to_cart'),
  path('cart/',CartView,name='cart_view'),
  path('cancel/<int:id>/',CancelOrder,name='cancel_order'),



  # ?orders


path('place_orders/',PlaceOrder,name='place_order'),
path('orders/',Orderview,name='order_view'),
path('clear/<int:id>/',ClearHistory,name='clear'),
path('clearall/',ClearAll,name='clearall'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




