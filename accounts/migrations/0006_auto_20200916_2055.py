# Generated by Django 3.1.1 on 2020-09-16 15:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200916_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetailsmodel',
            name='phone',
            field=models.BigIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
