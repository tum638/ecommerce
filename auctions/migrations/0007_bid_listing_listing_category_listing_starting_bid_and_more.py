# Generated by Django 4.0.4 on 2022-05-10 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_date_made'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=256)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='listing_category',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronic', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], default='Other', max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=264),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_listings', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_listings', to='auctions.bid'),
        ),
    ]
