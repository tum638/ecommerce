# Generated by Django 4.0.4 on 2022-05-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_listing_upload_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listing_category',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], default='Other', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='upload_image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]