from django.db import models

class Sellings(models.Model):
    f_image = models.ImageField(upload_to = 'media/sell')
    m_image = models.ImageField(upload_to = 'media/sell')
    b_image = models.ImageField(upload_to = 'media/sell')

    def register(self):
        self.save()