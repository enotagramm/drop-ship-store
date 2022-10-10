from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """Товар"""
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    code = models.CharField(max_length=255, verbose_name='Код товара')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена товара')
    unit = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ед. изм.')
    image_url = models.URLField(blank=True, null=True, verbose_name='Картинка')
    note = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} - {self.price}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Payment(models.Model):
    """Оплата"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='Сумма платежа')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания платежа')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.user} - {self.amount}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Order(models.Model):
    """Заказ"""
    STATUS_CART = '1_cart'
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART, verbose_name='Статус')
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='Сумма заказа')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания заказа')
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True,
                                verbose_name='Последний платеж')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.user} - {self.status}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    """Товар в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='Скидка')

    def __str__(self):
        return f'{self.product} - {self.price}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
