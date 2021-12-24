from django.db import models
from .product import Product
from .customer import Customer
import datetime

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=500, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default= datetime.datetime.today)
    city = models.CharField(max_length=100,default='Dharwad')
    landmark = models.CharField(max_length=150,default='Hanuman Temple')
    mode = models.CharField(max_length=50,default='Cash On Delivery')
    pin = models.IntegerField( default=580001)

    status = models.BooleanField(default=False)


    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order\
            .objects\
            .filter(customer = customer_id)\
            .order_by('-date')

    @staticmethod
    def get_orders_by_id(ids):
        return  Order.objects.filter(id__in = ids)

    @staticmethod
    def get_all_orders():
        return Order.objects.all()



