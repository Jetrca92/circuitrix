# Generated by Django 4.2.5 on 2023-10-25 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_race_racetrack_raceresult_race_location_race_teams_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceresult',
            name='best_lap',
            field=models.DurationField(),
        ),
    ]
