# Generated by Django 3.0.8 on 2020-09-10 22:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200909_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]