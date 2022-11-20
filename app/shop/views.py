from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import Item, Order, OrderItem
import stripe
import uuid


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {
            'item': instance,
            'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
        }
        return Response(context, template_name='shop/item.html')


class AddToCartDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        order = find_or_create_order(request)
        item = self.get_object()
        order_item, _ = OrderItem.objects.get_or_create(order=order, item=item)
        order_item.quantity += 1
        order_item.save()
        return Response({'Result': 'success'})


class BuyAPIView(APIView):

    def get(self, request, *args, **kwargs):
        order = find_or_create_order(request)
        order_items = OrderItem.objects.filter(order=order)
        line_items = self.produce_line_items(order_items)
        if line_items:
            session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:8000/item/1',
                cancel_url='http://localhost:8000/item/1',
            )
            return Response(session)
        else:
            return Response({'result': 'Cart is empty'})

    @staticmethod
    def produce_line_items(order_items: list[OrderItem]) -> list[dict]:
        line_items = []
        for order_item in order_items:
            item = order_item.item
            item_params = {
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': order_item.quantity,
            }
            line_items.append(item_params)

        return line_items


def find_or_create_order(request) -> Order:
    if request.user.is_authenticated:
        order, _ = Order.objects.get_or_create(
            user=request.user,
            ordered=False
        )
    elif request.session.get('session_key'):
        order, _ = Order.objects.get_or_create(
            session_key=request.session['session_key'],
            ordered=False
        )
    else:
        request.session['session_key'] = str(uuid.uuid1())
        order, _ = Order.objects.get_or_create(
            session_key=request.session['session_key'],
            ordered=False
        )

    return order

