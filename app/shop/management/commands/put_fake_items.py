from django.core.management.base import BaseCommand
from shop.models import Item
import random


class Command(BaseCommand):
    help = 'Команда для заполнения Items 10 продуктами из Stripe UI'

    def handle(self, *args, **options):
        for num in range(10):
            name = f'item {num}'
            description = f'Awesome item {num}'
            price = random.randint(100, 2000)
            Item.objects.get_or_create(
                name=name,
                description=description,
                price=price,
            )

