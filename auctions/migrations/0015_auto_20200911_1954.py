# Generated by Django 3.0.8 on 2020-09-11 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_watchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='max_bid',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
