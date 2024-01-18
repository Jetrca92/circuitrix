# Generated by Django 4.2.5 on 2024-01-18 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0030_driver_is_market_listed'),
        ('market', '0003_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverlisting',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_listing', to='manager.driver'),
        ),
    ]
