# Generated by Django 3.2 on 2021-05-03 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0015_auto_20210503_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellproduct',
            name='b_image',
            field=models.ImageField(upload_to='uploads/products/'),
        ),
        migrations.AlterField(
            model_name='sellproduct',
            name='f_image',
            field=models.ImageField(upload_to='uploads/products/'),
        ),
        migrations.AlterField(
            model_name='sellproduct',
            name='m_image',
            field=models.ImageField(upload_to='uploads/products/'),
        ),
    ]
