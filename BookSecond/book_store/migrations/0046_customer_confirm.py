# Generated by Django 3.2 on 2021-06-05 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0045_customer_cap'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='confirm',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
