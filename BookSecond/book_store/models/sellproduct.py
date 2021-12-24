from django.db import models
from .customer import Customer
import datetime

class SellProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=10)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    front_image = models.ImageField(upload_to='uploads/sell', default='')
    index_image = models.ImageField(upload_to='uploads/sell', default='')
    back_image = models.ImageField(upload_to='uploads/sell', default='')
    author = models.CharField(max_length=50)
    edition = models.CharField(max_length=20)
    city = models.CharField(max_length=20, default='Dharwad')
    state = models.CharField(max_length=20, default='Karnataka')
    pin  = models.IntegerField( default=580001)
    address = models.CharField(max_length=100,default='Dharwad')
    isbn = models.IntegerField(default=123456789123)
    phone = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    page = models.IntegerField(default=200)
    publisher = models.CharField(max_length=500, default='Rupa Publications')

    def reg(self):
        self.save()

    @staticmethod
    def get_sellings_by_customer(customer_id):
        return SellProduct \
            .objects \
            .filter(customer=customer_id) \
            .order_by('-date')

    def __str__(self):
        return self.name