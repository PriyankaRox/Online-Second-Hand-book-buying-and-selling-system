# Generated by Django 3.2 on 2021-06-02 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0037_auto_20210602_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=250),
        ),
    ]
