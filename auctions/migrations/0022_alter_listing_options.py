# Generated by Django 4.0.4 on 2022-05-16 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_watchlist_listing_watchlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ['-date_made']},
        ),
    ]
