from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import Item
import stripe

stripe.api_key = 'sk_test_51M5raYHRnVUW1L'


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'item': instance}, template_name='shop/item.html')


class BuyDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': instance.name,
                    },
                    'unit_amount': int(instance.price*100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        return Response(session)
