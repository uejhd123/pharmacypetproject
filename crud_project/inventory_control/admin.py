from django.contrib import admin


from .models import Warehouse, Product, ProductDescription, TotalSale, Customer, SaleToCustomer


admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(ProductDescription)
admin.site.register(TotalSale)
admin.site.register(Customer)
admin.site.register(SaleToCustomer)

