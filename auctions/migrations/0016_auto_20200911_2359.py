# Generated by Django 3.0.8 on 2020-09-11 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200911_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='ended',
            new_name='closed',
        ),
    ]
