# Generated by Django 3.0.8 on 2020-08-28 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_listed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
