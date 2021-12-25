from django.db import models
from authapp.models import CleanspotUser
from cartapp.models import Service, Cart
from mainapp.models import Premises


class Order(models.Model):
    """Заказ"""
    SEARCH_CLEANER = 'SC'
    CLEANER_IS_FOUND = 'CIF'
    PROCEEDED = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDERS_STATUS_CHOICES = (
        (SEARCH_CLEANER, 'поиск исполнителя'),
        (CLEANER_IS_FOUND, 'клинер найден'),
        (PROCEEDED, 'в работе'),
        (READY, 'завершен'),
        (CANCEL, 'отменен'),
    )

    client = models.ForeignKey(
        CleanspotUser,
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name='Заказчик',
        null=True,
        blank=True
    )
    session_key = models.CharField(
        max_length=1024,
        verbose_name='Ключ сессии',
        null=True,
        blank=True
    )

    cleaner = models.ForeignKey(
        CleanspotUser,
        on_delete=models.CASCADE,
        related_name='cleaner',
        verbose_name='Клинер',
        null=True,
        blank=True,
    )

    cart = models.ForeignKey(
        Cart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=3,
        choices=ORDERS_STATUS_CHOICES,
        default=SEARCH_CLEANER,
    )

    premise = models.ForeignKey(
        Premises,
        on_delete=models.CASCADE,
        verbose_name='Помещение',
        null=True,
        blank=True
    )

    comment = models.TextField(
        verbose_name='Комментарий к заказу',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'
