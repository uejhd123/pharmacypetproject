from django.urls import path
from . import views
from .views import login_view


urlpatterns = [
    # :TODO customize main page
    path('', views.products_view),
    path('products/', views.products_view, name='products'),
    path('api/products/', views.api_products, name='api_products'),
    path('expired/', views.expired_products_view, name='expired'),
    path('api/expired_products/', views.api_expired_products, name='api_products'),
    path('total_sale/', views.total_sale_view, name='total_sale'),
    path('customers/', views.customer_view, name='customers'),

    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<str:model>/<int:id>/', views.destroy, name='destroy'),

    path('add_warehouse/', views.add_warehouse, name='add_warehouse'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_product_description/', views.add_product_description, name='add_product_description'),
    path('add_customer/', views.add_customer, name='add_customer'),

    path('sell/', views.sell, name="sell"),
    path('get-product/', views.get_product, name="get_product"),
    path('get-customer/', views.get_customer, name="get_customer"),


    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
