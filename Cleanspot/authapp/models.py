
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from authapp.manager import CustomUserManager


class Cities(models.Model):
    name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name='Город',
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
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class CleanspotUserType(models.Model):
    """Класс описывающий модель типа пользователя"""
    name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        verbose_name='Название типа пользователя',
    )

    description = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Описание типа пользователя',
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
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Типы пользователей'

    def __str__(self):
        return self.name


class CleanspotUser(AbstractBaseUser, PermissionsMixin):
    """Класс описывающий модель пользователя"""
    user_type = models.ForeignKey(
        CleanspotUserType,
        on_delete=models.CASCADE,
        verbose_name='Тип пользователя',
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='E-mail',
    )

    title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Имя пользователя',
    )

    name_display_site = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Имя отображения на сайте',
    )

    inn_kpp = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='ИНН/КПП',
    )

    city = models.ForeignKey(
        Cities,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Город',
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type_id']

    # name = models.CharField(
    #     max_length=128,
    #     blank=True,
    #     null=True,
    #     verbose_name='Имя пользователя'
    # )

    is_staff = models.BooleanField(
        verbose_name='Moderator',
        default=False,
        help_text='Определяет разрешение пользователя на вход в административную часть.'
    )

    is_active = models.BooleanField(
        verbose_name='Active',
        default=False,
        help_text='Определяет активен ли пользователь в системе. Снимите флаг, '
                  'вместо удаления пользователя.'
    )

    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
        default=None,
        verbose_name='Номер телефона',)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения',
    )

    activation_key = models.CharField(
        max_length=128,
        blank=True
    )

    activation_key_expires = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
