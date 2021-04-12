# Generated by Django 3.1.5 on 2021-03-07 13:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210306_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='watchlist',
            field=models.ManyToManyField(related_name='user_watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
