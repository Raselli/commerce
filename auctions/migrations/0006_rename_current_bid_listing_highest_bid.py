# Generated by Django 4.0.3 on 2022-04-20 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_current_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='current_bid',
            new_name='highest_bid',
        ),
    ]