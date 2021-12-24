from django.db import models
from .customer import Customer

class Feedback(models.Model):
    title = models.CharField(max_length = 20, default='')
    description = models.CharField(max_length = 500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    quality = models.IntegerField(default=5)
    exp = models.IntegerField(default=8)

    def reg(self):
        self.save()

    def __str__(self):
        return self.title
