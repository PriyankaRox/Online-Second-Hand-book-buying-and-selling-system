# Generated by Django 3.2 on 2021-05-02 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0009_auto_20210502_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellproduct',
            name='customer',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='book_store.customer'),
        ),
    ]
