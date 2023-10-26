# Generated by Django 4.2.5 on 2023-10-26 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_laprecord_racetrack_lap_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laprecord',
            name='holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laprecord_holder', to='manager.driver'),
        ),
    ]
