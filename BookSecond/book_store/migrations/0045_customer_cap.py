# Generated by Django 3.2 on 2021-06-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0044_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cap',
            field=models.BooleanField(default=True),
        ),
    ]