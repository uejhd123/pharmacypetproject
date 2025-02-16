from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class ProductDescription(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class Product(models.Model):
    name = models.CharField(max_length=100)
    mfg = models.DateField()
    exp = models.DateField()
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    description = models.ForeignKey(ProductDescription, on_delete=models.CASCADE, related_name='product')

    def total_purchase_amount(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return self.name


class ExpiredProduct(models.Model):
    name = models.CharField(max_length=100)
    mfg = models.DateField()
    exp = models.DateField()
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    description = models.ForeignKey(ProductDescription, on_delete=models.CASCADE, related_name='expired_product')

    def total_purchase_amount(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return self.name


class TotalSale(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of Product {self.product_id} ({self.quantity} units)"


class Customer(models.Model):
    customer = models.CharField(max_length=50)
    mail = models.EmailField()

    def __str__(self):
        return self.customer


class SaleToCustomer(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    mfg = models.DateField()
    exp = models.DateField()
    sold_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer
