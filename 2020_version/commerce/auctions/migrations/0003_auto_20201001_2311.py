# Generated by Django 2.2.5 on 2020-10-02 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20201001_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='listing_id',
            new_name='listing',
        ),
    ]
