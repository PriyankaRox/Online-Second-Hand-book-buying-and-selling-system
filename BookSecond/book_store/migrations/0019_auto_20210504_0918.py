# Generated by Django 3.2 on 2021-05-04 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0018_auto_20210504_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellings',
            name='b_image',
            field=models.ImageField(upload_to='media/sell'),
        ),
        migrations.AlterField(
            model_name='sellings',
            name='f_image',
            field=models.ImageField(upload_to='media/sell'),
        ),
        migrations.AlterField(
            model_name='sellings',
            name='m_image',
            field=models.ImageField(upload_to='media/sell'),
        ),
    ]
