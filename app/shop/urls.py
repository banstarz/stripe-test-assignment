from django.urls import path
from .views import ItemDetail, BuyAPIView, AddToCartDetail

urlpatterns = [
    path('item/<int:pk>/', ItemDetail.as_view(), name='item'),
    path('add_to_cart/<int:pk>/', AddToCartDetail.as_view(), name='add_to_cart'),
    path('buy/', BuyAPIView.as_view(), name='buy'),
]