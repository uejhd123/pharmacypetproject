from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.db.models import Count
from django.db import transaction

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm, WarehouseForm, ProductDescriptionForm, CustomerForm
from .models import Product, Warehouse, TotalSale, Customer, SaleToCustomer, ProductDescription, ExpiredProduct

from django.utils import timezone
from datetime import date


@login_required
def products_view(request):
    products = Product.objects.select_related('description').all()
    warehouses = Warehouse.objects.all()
    context = {
        'title': 'Таблица всех складов',
        'products': products,
        'warehouses': warehouses,
    }
    return render(request, 'products.html', context)


@login_required()
def expired_products_view(request):
    expired_products = ExpiredProduct.objects.select_related('description').all()
    warehouses = Warehouse.objects.all()
    context = {
        'title': 'Таблица всех складов с просроченной продукцией',
        'expired_products': expired_products,
        'warehouses': warehouses,
    }
    return render(request, 'expired_products.html', context)


@login_required
def total_sale_view(request):
    total_sales = TotalSale.objects.all()

    # Подсчет общих значений
    total_quantity = sum(sale.quantity for sale in total_sales)
    total_price = sum(sale.price for sale in total_sales)
    total_sum = sum(sale.total for sale in total_sales)

    context = {
        'title': 'Таблица продаж',
        'total_sales': total_sales,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
    }
    return render(request, 'total_sale.html', context)


@login_required
def customer_view(request):
    customers = Customer.objects.all()

    context = {
        'title': 'Таблица покупателей',
        'customers': customers,
    }
    return render(request, 'customer.html', context)


@login_required
def get_product_data(products):
    product_list = []
    for product in products:
        description = product.description.description if hasattr(product, 'description') else 'Нет описания'
        product_list.append({
            'id': product.id,
            'name': product.name,
            'description': description,
            'quantity': product.quantity,
            'price_per_unit': str(product.price_per_unit),
            'total_purchase_amount': str(product.total_purchase_amount()),
            'mfg': product.mfg.strftime('%Y-%m-%d'),
            'exp': product.exp.strftime('%Y-%m-%d')
        })
    return product_list


@login_required
def api_products(request):
    warehouse_id = request.GET.get('warehouse_id')
    if warehouse_id:
        products = Product.objects.filter(warehouse_id=warehouse_id).select_related('description')
    else:
        products = Product.objects.all().select_related('description')

    product_list = get_product_data(products)

    return JsonResponse({'products': product_list})


@login_required
def api_expired_products(request):
    warehouse_id = request.GET.get('warehouse_id')
    today = date.today()

    if warehouse_id:
        expired_products = ExpiredProduct.objects.filter(warehouse_id=warehouse_id, exp__lt=today).select_related(
            'description')
    else:
        expired_products = ExpiredProduct.objects.filter(exp__lt=today).select_related('description')

    expired_product_list = get_product_data(expired_products)

    return JsonResponse({'expired_products': expired_product_list})


@login_required
def edit(request, id):
    product = get_object_or_404(Product, id=id)
    product_description = product.description

    warehouses = Warehouse.objects.all()
    descriptions = ProductDescription.objects.all()

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.mfg = request.POST.get('mfg')
        product.exp = request.POST.get('exp')
        product.quantity = request.POST.get('quantity')
        product.price_per_unit = request.POST.get('price_per_unit')
        warehouse_id = request.POST.get('warehouse')
        product.warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        product.save()

        description_id = request.POST.get('description')
        if description_id:
            product.description = get_object_or_404(ProductDescription, id=description_id)
        product.save()

        # Проверка ошибок и добавление сообщений об ошибке
        form_errors = {}
        for field in ['name', 'mfg', 'exp', 'quantity', 'price_per_unit', 'warehouse']:
            if not request.POST.get(field):
                form_errors[field] = f"{field.capitalize()} не может быть пустым"
        if form_errors:
            error_message = 'Пожалуйста, исправьте следующие ошибки:'
            for field, error in form_errors.items():
                error_message += f'\n{error}'
            messages.error(request, error_message)
            context = {
                'title': 'Изменение данных',
                'product': product,
                'product_description': product_description,
                'warehouses': warehouses,
                'descriptions': descriptions,
            }
            return render(request, 'edit.html', context)
        messages.success(request, 'Данные успешно обновлены.')
        return redirect(f'/edit/{id}')

    context = {
        'title': 'Изменение данных',
        'product': product,
        'product_description': product_description,
        'warehouses': warehouses,
        'descriptions': descriptions,
    }

    return render(request, 'edit.html', context)


@login_required
def destroy(request, model, id):
    if model == 'product':
        try:
            item = Product.objects.get(id=id)
            item.delete()
            messages.success(request, "Запись успешно удалена.")
        except Product.DoesNotExist:
            messages.error(request, "Запись не найдена.")
        return redirect('/products')
    elif model == 'expired_product':
        try:
            item = ExpiredProduct.objects.get(id=id)
            item.delete()
            messages.success(request, "Запись успешно удалена.")
        except ExpiredProduct.DoesNotExist:
            messages.error(request, "Запись не найдена.")
        return redirect('/expired')
    else:
        messages.error(request, "Неверная модель.")

    return redirect('/')


@login_required
def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Склад успешно добавлен.')
            return redirect('add_warehouse')  # Перенаправление на текущую страницу
        else:
            errors = {}
            field_names_mapping = {
                'warehouse': 'Склад',
            }
            for field in form:
                if field.errors:
                    field_name_ru = field_names_mapping.get(field.name, field.name)
                    errors[field_name_ru] = field.errors.as_text()
            error_message = 'Пожалуйста, исправьте ошибки в форме:'
            for field, error in errors.items():
                error_message += f'\n{field}: {error}'
            messages.error(request, error_message)
    else:
        form = WarehouseForm()
    context = {
        'title': 'Добавить склад',
        'form': form
    }
    return render(request, 'add_warehouse.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно добавлен.')
            return redirect('/add_product')  # :TODO edit this to actual URL
        else:
            errors = {}
            field_names_mapping = {
                'name': 'Название',
                'mfg': 'Дата производства',
                'exp': 'Срок годности',
                'quantity': 'Количество',
                'price_per_unit': 'Цена за единицу',
                'warehouse': 'Склад',
                'description': 'Описание'
            }
            for field in form:
                if field.errors:
                    field_name_ru = field_names_mapping.get(field.name, field.name)
                    errors[field_name_ru] = field.errors.as_text()
            error_message = 'Пожалуйста, исправьте ошибки в форме:'
            for field, error in errors.items():
                error_message += f'\n{field}: {error}'
            messages.error(request, error_message)
    else:
        form = ProductForm()

    context = {
        'title': 'Добавить продукцию',
        'form': form
    }
    return render(request, 'add_product.html', context)


@login_required
def add_product_description(request):
    if request.method == 'POST':
        form = ProductDescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Описание успешно добавлено.')
            return redirect('/add_product_description')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductDescriptionForm()
    context = {
        'title': 'Добавить описание',
        'form': form
    }
    return render(request, 'add_product_description.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно добавлен.')
            return redirect('/add_customer')  # :TODO edit this to actual URL
        else:
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.label] = field.errors.as_text()
            error_message = 'Пожалуйста, исправьте ошибки в форме:'
            for field, error in errors.items():
                error_message += f'\n{field}: {error}'
            messages.error(request, error_message)
    else:
        form = CustomerForm()

    context = {
        'title': 'Добавить клиента',
        'form': form
    }
    return render(request, 'add_customer.html', context)


@login_required
def get_product(request):
    warehouse_id = request.GET['warehouse_id']
    get_warehouse = Warehouse.objects.get(id=warehouse_id)
    product = Product.objects.filter(warehouse=get_warehouse, quantity__gt=0)
    return render(request, 'get-product.html', {'products': product})


@login_required
def get_customer(request):
    customer_id = request.GET['customer_id']
    get_customer_data = Customer.objects.get(id=customer_id)
    customer = Product.objects.filter(warehouse=get_customer_data)
    return render(request, 'get-product.html', {'customers': customer})


@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def sell(request):
    if request.method == 'POST':
        data = request.POST
        warehouse_ids = data.getlist('warehouse')
        product_ids = data.getlist('product')
        quantities = data.getlist('quantity')
        customer = data.get('customer')

        errors = {}
        if not customer or customer == '0':
            errors['customer'] = 'Выберите покупателя.'

        for i in range(len(product_ids)):
            if product_ids[i] == '0':
                errors[f'product_{i}'] = 'Выберите товар.'
            if warehouse_ids[i] == '0':
                errors[f'warehouse_{i}'] = 'Выберите склад.'
            if not quantities[i] or int(quantities[i]) < 1:
                errors[f'quantity_{i}'] = 'Введите допустимое количество.'

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        try:
            for i in range(len(product_ids)):
                product_id = int(product_ids[i])
                quantity = int(quantities[i])

                product = Product.objects.select_for_update().get(id=product_id)
                if product.quantity < quantity:
                    errors[f'quantity_{i}'] = 'Недостаточное количество товара.'
                    raise ValueError('Insufficient quantity')

                product.quantity -= quantity
                product.save()

                total_sale, created = TotalSale.objects.get_or_create(product_id=product_id, defaults={
                    'name': product.name,
                    'quantity': 0,
                    'price': product.price_per_unit,
                    'total': 0,
                    'updated_at': timezone.now()
                })

                total_sale.quantity += quantity
                total_sale.total += (quantity * product.price_per_unit)
                total_sale.updated_at = timezone.now()
                total_sale.save()

                SaleToCustomer.objects.create(
                    product_id=product_id,
                    quantity=quantity,
                    price_per_unit=product.price_per_unit,
                    total=(quantity * product.price_per_unit),
                    mfg=product.mfg,
                    exp=product.exp,
                    sold_at=timezone.now(),
                    customer_id=customer
                )
            messages.success(request, 'Товары успешно проданы.')
            return JsonResponse({'success': True}, status=200)
        except ValueError:
            return JsonResponse({'errors': errors}, status=400)

    else:
        warehouses = Warehouse.objects.annotate(
            num_products=Count('product')).filter(
            num_products__gt=0,
            product__quantity__gt=0).distinct()
        customers = Customer.objects.all()
        context = {
            'title': 'Продажа',
            'warehouses': warehouses,
            'customers': customers,
        }
        return render(request, 'sell.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', 'off') == 'on'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:

                request.session.set_expiry(0)

            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Данные не верны'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')
