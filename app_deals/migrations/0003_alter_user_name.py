# Generated by Django 4.2.3 on 2023-07-12 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_deals', '0002_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
    ]