# Generated by Django 4.1.2 on 2022-10-10 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1_cart', 'cart'), ('2_waiting_for_payment', 'waiting_for_payment'), ('3_paid', 'paid')], default='1_cart', max_length=32, verbose_name='Статус')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Сумма заказа')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Время создания заказа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование товара')),
                ('code', models.CharField(max_length=255, verbose_name='Код товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Цена товара')),
                ('unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ед. изм.')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Картинка')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Сумма платежа')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Время создания платежа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Цена')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Скидка')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product', verbose_name='Товар')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.payment', verbose_name='Последний платеж'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
