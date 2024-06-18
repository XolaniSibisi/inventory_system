from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from accounts.models import Product

class Command(BaseCommand):
    help = 'Check and send low stock alerts'

    def handle(self, *args, **kwargs):
        low_stock_products = Product.objects.filter(quantity__lt=10)

        for product in low_stock_products:
            send_mail(
                'Low Stock Alert',
                f'The stock for {product.name} is running low.',
                'your@email.com',
                ['farmer@email.com'],
            )