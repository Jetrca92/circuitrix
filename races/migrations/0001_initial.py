# Generated by Django 4.2.5 on 2023-10-21 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manager', '0007_remove_team_car_team_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('laps', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Racetrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('lap_length_km', models.FloatField()),
                ('total_laps', models.PositiveIntegerField()),
                ('straights', models.FloatField()),
                ('slow_corners', models.FloatField()),
                ('fast_corners', models.FloatField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.country')),
            ],
        ),
        migrations.CreateModel(
            name='RaceResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('best_lap', models.TimeField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='races.race')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.team')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.racetrack'),
        ),
        migrations.AddField(
            model_name='race',
            name='teams',
            field=models.ManyToManyField(related_name='races', to='manager.team'),
        ),
        migrations.CreateModel(
            name='Championship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('races', models.ManyToManyField(blank=True, related_name='league_races', to='races.race')),
                ('teams', models.ManyToManyField(blank=True, related_name='league_teams', to='manager.team')),
            ],
        ),
    ]
