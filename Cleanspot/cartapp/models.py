from django.db import models
from django.utils.text import slugify

from authapp.models import CleanspotUser
from common.const import CLEANING_TIME_CHOICES, MORNING


class UserTypeForServiceType(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Название типа пользователя',
    )

    description = models.CharField(
        max_length=128,
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

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL',
        db_index=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тип пользователя для типа услуг'
        verbose_name_plural = 'Типы пользователей для типов услуг'

    def save(self, *args, **kwargs):
        # Если типа пользователя еще нет и он только создается мы сразу присваиваем ему slug
        if not self.id:
            self.slug = slugify(self.name)
        super(UserTypeForServiceType, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class ServiceType(models.Model):
    """Класс описывающий типы улуг"""
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Название типа услуг',
    )

    description = models.CharField(
        max_length=128,
        verbose_name='Описание типа пользователя',
        blank=True,
    )

    user_type_for_service_type = models.ForeignKey(
        UserTypeForServiceType,
        on_delete=models.CASCADE,
        verbose_name='Тип пользователя для типа услуг',
        null=True,
        related_name='user_type_for_service_types'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения',
    )

    slug = models.SlugField(
        max_length=255,
        verbose_name='URL',
        db_index=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тип услуг'
        verbose_name_plural = 'Типы услуг'

    def save(self, *args, **kwargs):
        # Если типа услуг еще нет и он только создается мы сразу присваиваем ему slug
        if not self.id:
            self.slug = slugify(self.name)
        super(ServiceType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_type_for_service_type.description}: {self.description}'


class Service(models.Model):
    """Класс описывающий услуги"""
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

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена'
    )
    basic_service = models.BooleanField(
        verbose_name='Основная услуга',
        default=False)
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


class CartService(models.Model):
    user = models.ForeignKey(
        CleanspotUser,
        verbose_name='Покупатель',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        "Cart",
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='cartitems'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
    )
    session_key = models.CharField(
        max_length=1024,
        verbose_name='Ключ сессии',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество услуг',
        default=1
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
        verbose_name = 'Услуга для корзины'
        verbose_name_plural = 'Услуги для корзин'

    def __str__(self):
        return f'Продукт: {self.service.name} для корзины №{self.cart.id}'

    @property
    def get_servise_cost(self):
        return self.service.price * self.quantity


class DaysOfWeek(models.Model):

    title = models.CharField(max_length=20, blank=True, null=True)
    short_title = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'

    def __str__(self):
        return self.short_title


class WindowWashing(models.Model):
    num_windows = models.PositiveIntegerField(verbose_name='Количество окон', blank=True, null=True)
    num_window_frame = models.PositiveIntegerField(verbose_name='Количество створок окон', blank=True, null=True)
    num_stained_windows = models.PositiveIntegerField(verbose_name='Количество витражных окон', blank=True, null=True)
    num_stained_window_frame = models.PositiveIntegerField(verbose_name='Количество створок витражных окон',
                                                           blank=True, null=True)
    num_showcase = models.PositiveIntegerField(verbose_name='Количество витрин', blank=True, null=True)
    square_windows = models.PositiveIntegerField(verbose_name='Площадь остекления окон', blank=True, null=True)
    square_showcase = models.PositiveIntegerField(verbose_name='Площадь остекления витрин', blank=True, null=True)
    height_showcase = models.PositiveIntegerField(verbose_name='Высота витрин', blank=True, null=True)
    cart = models.ForeignKey("Cart", verbose_name='Корзина', on_delete=models.CASCADE, related_name='cartwindows',
                             null=True)

    def __str__(self):
        return f'Мойка окон для корзины №{self.cart.id}'


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey(
        CleanspotUser,
        verbose_name='Покупатель',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    services = models.ManyToManyField(
        CartService,
        blank=True,
        verbose_name='Услуга для корзины',
        related_name='related_cart',
    )
    windows = models.ManyToManyField(
        WindowWashing,
        verbose_name='Мойка окон',
        blank=True,
        related_name='related_cart_window'
    )
    is_windows = models.BooleanField(default=False)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Общая цена'
    )
    comment = models.TextField(
        verbose_name='Комментарий к заказу',
        null=True,
        blank=True
    )
    cleaning_days = models.ManyToManyField(
        DaysOfWeek,
        blank=True,
        verbose_name='День недели',
    )

    cleaning_time = models.CharField(
        verbose_name='Время уборки',
        max_length=15,
        choices=CLEANING_TIME_CHOICES,
        blank=True,
    )

    number_stuff = models.PositiveIntegerField(
        verbose_name='Количество персонала',
        default=1,
        blank=True,
        null=True
    )
    in_order = models.BooleanField(default=False)
    session_key = models.CharField(
        max_length=1024,
        verbose_name='Ключ сессии',
        null=True,
        blank=True
    )
    date_order = models.DateField(
        verbose_name='Дата выполнения заказа',
        blank=True,
        null=True,
    )
    is_other_date = models.BooleanField(default=False, verbose_name='Готов рассмотреть другие даты уборки')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения',
    )

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        self.total_price = self.cartitems.select_related()
        return sum(list(map(lambda x: x.get_service_cost, self.total_price)))
