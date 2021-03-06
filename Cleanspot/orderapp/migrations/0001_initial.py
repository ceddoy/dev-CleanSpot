# Generated by Django 3.2.7 on 2021-11-07 12:05

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
                ('status', models.CharField(choices=[('SC', 'поиск исполнителя'), ('CIF', 'клинер найден'), ('PD', 'в работе'), ('RDY', 'завершен'), ('CNC', 'отменен')], default='SC', max_length=3, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('cleaner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cleaner', to=settings.AUTH_USER_MODEL, verbose_name='Клинер')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название типа услуг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
            ],
            options={
                'verbose_name': 'Тип услуг',
                'verbose_name_plural': 'Типы услуг',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название услуги')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.servicetype', verbose_name='Тип услуги')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.order', verbose_name='Заказ')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Услуга заказа',
                'verbose_name_plural': 'Услуги заказа',
            },
        ),
    ]
