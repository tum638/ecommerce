# Generated by Django 4.0.4 on 2022-05-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listing_image_url_listing_upload_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='upload_image',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]