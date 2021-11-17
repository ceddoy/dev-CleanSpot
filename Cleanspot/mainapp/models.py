from django.db import models
from authapp.models import CleanspotUser, Cities


class PremisesType(models.Model):
    name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name='Тип помещения',
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
        verbose_name = 'Тип помещения'
        verbose_name_plural = 'Типы помещений'

    def __str__(self):
        return self.name


class Premises(models.Model):
    premises_owner = models.ForeignKey(
        CleanspotUser,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Владелец помещения',
    )

    premises_city = models.ForeignKey(
        Cities,
        on_delete=models.CASCADE,
        verbose_name='Город',
    )

    premises_type = models.ForeignKey(
        PremisesType,
        on_delete=models.CASCADE,
        verbose_name='Тип помещения',
    )

    premises_street = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name='Улица',
    )

    premises_house_num = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        verbose_name='Номер дома',
    )

    premises_apartment = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Квартира',
    )

    premises_intercom = models.CharField(
        max_length=5,
        blank=True,
        verbose_name='Домофон',
    )

    premises_entrance = models.CharField(
        max_length=2,
        blank=True,
        verbose_name='Подъезд',
    )

    premises_floor = models.CharField(
        max_length=3,
        blank=True,
        verbose_name='Этаж',
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
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def get_address(self):
        if self.premises_apartment:
            apartment = f', кв.{self.premises_apartment}'
        else:
            apartment = ''
        if self.premises_entrance:
            entrance = f', под. {self.premises_entrance}'
        else:
            entrance = ''
        address = f'{self.premises_city}, ул.{self.premises_street}, д.{self.premises_house_num}' \
                  f'{apartment}{entrance}'
        return address

    def __str__(self):
        return self.get_address()
