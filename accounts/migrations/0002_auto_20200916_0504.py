# Generated by Django 3.1.1 on 2020-09-15 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfermoneytransactionsmodel',
            old_name='user',
            new_name='from_user',
        ),
    ]