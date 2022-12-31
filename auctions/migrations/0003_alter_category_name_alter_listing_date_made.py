# Generated by Django 4.0.4 on 2022-05-10 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronic', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], max_length=12),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_made',
            field=models.DateField(default=datetime.datetime(2022, 5, 10, 15, 26, 36, 115909)),
        ),
    ]
