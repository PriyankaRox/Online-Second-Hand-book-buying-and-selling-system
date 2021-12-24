
from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.sellproduct import SellProduct
from .models.feedback import Feedback
from .models.video import Video


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'description', 'image']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminOrder(admin.ModelAdmin):
    list_display = ['product']



# Register your models here.
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer)
admin.site.register(Order, AdminOrder)
admin.site.register(SellProduct)
admin.site.register(Feedback)
admin.site.register(Video)
