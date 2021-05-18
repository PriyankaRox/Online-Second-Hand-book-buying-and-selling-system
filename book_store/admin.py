from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Category
from .models import Customer
from .models import Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['category', 'title', 'price', 'author', 'description', 'ISBN', 'language', 'publisher', 'edition', 'pages', 'format', 'image']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'password']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Order)
