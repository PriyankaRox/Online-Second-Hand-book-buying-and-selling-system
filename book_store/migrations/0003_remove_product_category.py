# Generated by Django 3.2 on 2021-04-23 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0002_auto_20210424_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]