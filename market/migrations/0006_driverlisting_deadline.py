# Generated by Django 4.2.5 on 2024-01-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_alter_bid_bidder_alter_bid_driver_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverlisting',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
    ]