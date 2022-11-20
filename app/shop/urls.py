from django.urls import path
from .views import ItemDetail, BuyDetail

urlpatterns = [
    path('item/<int:pk>/', ItemDetail.as_view(), name='item'),
    path('buy/<int:pk>/', BuyDetail.as_view(), name='buy'),
]