# Generated by Django 3.0.8 on 2020-08-28 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200828_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='starting_bid',
        ),
    ]
