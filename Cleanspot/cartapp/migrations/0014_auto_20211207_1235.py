# Generated by Django 3.2.8 on 2021-12-07 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0013_auto_20211207_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('short_title', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
            },
        ),
        migrations.AlterField(
            model_name='cart',
            name='cleaning_days',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cartapp.daysofweek', verbose_name='День недели'),
        ),
    ]
