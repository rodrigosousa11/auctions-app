# Generated by Django 5.0.1 on 2024-01-31 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]