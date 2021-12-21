# Generated by Django 3.2.8 on 2021-12-07 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0016_auto_20211207_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cleaning_days',
        ),
        migrations.AddField(
            model_name='cart',
            name='cleaning_days',
            field=models.ManyToManyField(blank=True, null=True, to='cartapp.DaysOfWeek', verbose_name='День недели'),
        ),
    ]
