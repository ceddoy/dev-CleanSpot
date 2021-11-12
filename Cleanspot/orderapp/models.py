from django.db import models
from authapp.models import CleanspotUser


# Класс описывающий типы улуг
class ServiceType(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Название типа услуг',
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
        verbose_name = 'Тип услуг'
        verbose_name_plural = 'Типы услуг'

    def __str__(self):
        return self.name


# Класс описывающий услуги
class Service(models.Model):
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Тип услуги',
    )

    name = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Название услуги',
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
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Order(models.Model):
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
    )

    cleaner = models.ForeignKey(
        CleanspotUser,
        on_delete=models.CASCADE,
        related_name='cleaner',
        verbose_name='Клинер',
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=3,
        choices=ORDERS_STATUS_CHOICES,
        default=SEARCH_CLEANER,
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


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
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
        verbose_name = 'Услуга заказа'
        verbose_name_plural = 'Услуги заказа'

    def __str__(self):
        return f'{self.order}, услуга - {self.service}'
