# Generated by Django 4.2.5 on 2023-10-26 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_championship_racetracks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='racetrack',
            name='lap_record',
        ),
    ]