# Generated by Django 3.1.1 on 2020-09-15 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200916_0508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfermoneytransactionsmodel',
            old_name='from_user',
            new_name='user',
        ),
    ]
