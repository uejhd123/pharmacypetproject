from datetime import date

from celery import shared_task
from .models import Product, ExpiredProduct


@shared_task
def check_and_move_expired_products():
    expired_products = Product.objects.filter(exp__lt=date.today())
    for product in expired_products:
        try:

            ExpiredProduct.objects.create(
                name=product.name,
                mfg=product.mfg,
                exp=product.exp,
                quantity=product.quantity,
                price_per_unit=product.price_per_unit,
                warehouse=product.warehouse,
                description=product.description
            )
            print(f"ExpiredProduct created for {product.name}")
            product.delete()
        except Exception as e:

            print(f"Error creating ExpiredProduct for {product.name}: {str(e)}")
