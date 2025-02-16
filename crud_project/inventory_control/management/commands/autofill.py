from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from inventory_control.models import Warehouse, Product, ProductDescription, TotalSale, Customer, SaleToCustomer

materials_dict = {
    'мг': ['Алмаг ', 'Гептрал ', 'Креон ', 'Микразим ', 'Гиалуроновая кислота', 'Optipro ', 'Простамол Уно', 'Ренни ',
           'Пантодерм '],
    'шт': ['Туринабол', 'Спазмалгон', 'Эстракт тестестерона', 'фенабол', 'Караболин', 'Рисастерон', 'Киласит',
           'Сумарит', 'Чамарон'],
    'пара': ['Печерил', 'Галвус ', 'Бинт Peha-haft', 'Азарга ', 'Tena Прокладки', ' Унипласт', 'очки', 'бинт']
}


def populate_warehouses(count, fake):
    warehouses = []

    for _ in range(count):
        warehouse = Warehouse(
            name=fake.company()
        )
        warehouses.append(warehouse)

    Warehouse.objects.bulk_create(warehouses)


class Command(BaseCommand):
    help = 'Populate database with random entries. Usage: python manage.py autofill <count> <data_table_name>'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=5, help='Number of random entries to create')
        parser.add_argument('data_table_name', nargs='?', type=str, default='Product',
                            help='Data table name to populate')

    def handle(self, *args, **options):
        count = options['count']
        data_table_name = options['data_table_name']
        if count < 1:
            raise CommandError('Count should be a positive integer')

        fake = Faker('ru_RU')

        if data_table_name.lower() == 'product':
            self.populate_product(count, fake)
        elif data_table_name.lower() == 'productdescription':
            self.populate_product_description(count, fake)
        elif data_table_name.lower() == 'totalsale':
            self.populate_total_sale(count)
        elif data_table_name.lower() == 'customer':
            self.populate_customer(count, fake)
        elif data_table_name.lower() == 'saletocustomer':
            self.populate_sale_to_customer(count)
        elif data_table_name.lower() == 'warehouse':
            populate_warehouses(count, fake)
        else:
            raise CommandError('Invalid data table name')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated database with {count} entries in {data_table_name}'))

    @staticmethod
    def populate_product(count, fake):
        products = []
        warehouses = list(Warehouse.objects.all())
        descriptions = list(ProductDescription.objects.all())

        for _ in range(count):
            random_material = random.choice(materials_dict[random.choice(list(materials_dict.keys()))])
            mfg_date = fake.date_between(start_date='-3y', end_date='-1y')
            exp_date = mfg_date + timedelta(days=random.randint(365, 730))
            warehouse = random.choice(warehouses)
            description = random.choice(descriptions) if descriptions else ProductDescription.objects.create(
                description=fake.text(max_nb_chars=75)
            )

            product = Product(
                name=random_material,
                mfg=mfg_date,
                exp=exp_date,
                quantity=random.randint(1, 100),
                price_per_unit=round(random.uniform(100, 20000), 2),
                warehouse=warehouse,
                description=description
            )
            products.append(product)

        Product.objects.bulk_create(products)

    @staticmethod
    def populate_product_description(count, fake):
        descriptions = []

        for _ in range(count):
            description = ProductDescription(
                description=fake.text(max_nb_chars=75)
            )
            descriptions.append(description)

        ProductDescription.objects.bulk_create(descriptions)

    @staticmethod
    def populate_total_sale(count):
        sales = []
        products = list(Product.objects.all())

        for _ in range(count):
            product = random.choice(products)
            quantity = random.randint(1, product.quantity)
            total_sale = TotalSale(
                product_id=product.id,
                name=product.name,
                quantity=quantity,
                price=product.price_per_unit,
                total=round(quantity * product.price_per_unit, 2)
            )
            sales.append(total_sale)
        TotalSale.objects.bulk_create(sales)

    @staticmethod
    def populate_customer(count, fake):
        customers = []

        for _ in range(count):
            customer = Customer(
                customer=fake.name(),
                mail=fake.email()
            )
            customers.append(customer)

        Customer.objects.bulk_create(customers)

    @staticmethod
    def populate_sale_to_customer(count):
        sales_to_customers = []
        customers = list(Customer.objects.all())
        products = list(Product.objects.all())

        for _ in range(count):
            product = random.choice(products)
            customer = random.choice(customers)
            quantity = random.randint(1, product.quantity)
            sale_to_customer = SaleToCustomer(
                product_id=product.id,
                quantity=quantity,
                price_per_unit=product.price_per_unit,
                total=round(quantity * product.price_per_unit, 2),
                mfg=product.mfg,
                exp=product.exp,
                customer=customer
            )
            sales_to_customers.append(sale_to_customer)

        SaleToCustomer.objects.bulk_create(sales_to_customers)
