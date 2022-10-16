from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


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

    @staticmethod
    def get_balance(user: User):    # метод получения баланса
        amount = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


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

    @staticmethod
    def get_cart(user: User): # Получение корзины и вернуть назад
        cart = Order.objects.filter(user=user, status=Order.STATUS_CART).first()
        if cart and (timezone.now() - cart.creation_time).days > 7:     # если корзина существует больше 7 дней
            cart.delete()   # она удаляется
            cart = None     # обнуляем корзину
        if not cart:
            cart = Order.objects.create(user=user, status=Order.STATUS_CART, amount=0)
        return cart

    def get_amount(self):   # получение суммы
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

    def make_order(self):   # создание заказа
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()
            auto_payment_unpaid_orders(self.user)

    @staticmethod
    def get_amount_of_unpaid_orders(user: User):    # получение суммы неоплаченных заказов
        amount = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT,
                                      ).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


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

    @property
    def amount(self):
        return self.quantity * (self.price - self.discount)


@transaction.atomic()
def auto_payment_unpaid_orders(user: User):     # функция автоплатежа
    unpaid_orders = Order.objects.filter(user=user,
                                         status=Order.STATUS_WAITING_FOR_PAYMENT)
    for order in unpaid_orders:
        if Payment.get_balance(user) < order.amount:
            break
        order.payment = Payment.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Payment.objects.create(user=user,
                               amount=-order.amount)


@receiver(post_save, sender=OrderItem)  # сигнал сохранения
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)   # сигнал удаления
def recalculate_order_amount_after_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_save, sender=Payment)  # сигнал сохранения
def auto_payment(sender, instance, **kwargs):
    user = instance.user
    auto_payment_unpaid_orders(user)
