# Generated by Django 3.0.8 on 2020-09-09 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200906_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='commented_by',
            new_name='bids_by',
        ),
    ]
