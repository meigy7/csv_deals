# Generated by Django 4.2.3 on 2023-07-10 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File_load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(blank=True, null=True, upload_to='deals', verbose_name='Файл CSV')),
            ],
        ),
        migrations.CreateModel(
            name='Gem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_deal', models.DateTimeField(verbose_name='Время сделки')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('spent_money', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма покупки')),
                ('csv_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_deals.file_load', verbose_name='Файл CSV')),
                ('gem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_deals.gem', verbose_name='Камень')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_deals.user', verbose_name='Пользователь')),
            ],
        ),
    ]
