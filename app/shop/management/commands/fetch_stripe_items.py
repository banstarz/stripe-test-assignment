from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Item
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Команда для заполнения Items 10 продуктами из Stripe UI'

    def handle(self, *args, **options):
        prices = stripe.Price.list(limit=100, expand=['data.product'])
        for price in prices['data']:
            product = price.get('product', {})
            name = product.get('name', 'undefined')
            description = product.get('description', 'empty')
            price = price.get('unit_amount')/100
            Item.objects.get_or_create(
                name=name,
                description=description,
                price=price,
            )

