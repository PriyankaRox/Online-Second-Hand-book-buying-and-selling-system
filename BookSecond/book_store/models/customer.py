from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    confirm = models.CharField(max_length=500)
    address = models.CharField(max_length=100, default='Kittle College road line bazar opposite national lodge', blank=True)
    city = models.CharField(max_length=100, default='Dharwad')
    landmark = models.CharField(max_length=150, default='Hanuman Temple')
    pin = models.IntegerField(default=580001)
    cap = models.BooleanField(default=True)

    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return  True
        else:
            return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

    @staticmethod
    def get_customer_by_id(ids):
        return Customer.objects.filter(id__in=ids)

    def __str__(self):
        return self.first_name
