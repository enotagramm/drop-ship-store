# Generated by Django 4.1.2 on 2022-10-19 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=255, verbose_name='Код товара'),
        ),
    ]
