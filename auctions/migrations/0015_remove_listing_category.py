# Generated by Django 5.0.1 on 2024-01-31 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_category_delete_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
    ]
