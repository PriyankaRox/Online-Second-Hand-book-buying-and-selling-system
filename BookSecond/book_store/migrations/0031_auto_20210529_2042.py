# Generated by Django 3.2 on 2021-05-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0030_auto_20210529_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='edition',
            field=models.CharField(default='Febrauary 2018', max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='language',
            field=models.CharField(default='English', max_length=500),
        ),
    ]
