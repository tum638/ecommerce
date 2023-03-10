# Generated by Django 4.0.4 on 2022-05-10 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_listing_listing_category_listing_starting_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=20.0, on_delete=django.db.models.deletion.CASCADE, related_name='bid_listings', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronic', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default='Other', on_delete=django.db.models.deletion.CASCADE, related_name='category_listings', to='auctions.category', to_field='name'),
        ),
    ]
