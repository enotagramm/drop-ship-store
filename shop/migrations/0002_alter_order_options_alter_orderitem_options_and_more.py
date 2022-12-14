# Generated by Django 4.1.2 on 2022-10-18 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['pk'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['pk'], 'verbose_name': 'Товар в заказе', 'verbose_name_plural': 'Товары в заказе'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['pk'], 'verbose_name': 'Оплата', 'verbose_name_plural': 'Оплаты'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['pk'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=255, verbose_name='Код товара'),
        ),
    ]
