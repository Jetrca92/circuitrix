# Generated by Django 4.2.5 on 2023-10-05 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_team_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('date_of_birth', models.DateTimeField()),
                ('experience', models.PositiveIntegerField(default=0)),
                ('skill_overall', models.PositiveIntegerField()),
                ('skill_racecraft', models.PositiveIntegerField()),
                ('skill_pace', models.PositiveIntegerField()),
                ('skill_focus', models.PositiveIntegerField()),
                ('skill_car_management', models.PositiveIntegerField()),
                ('skill_feedback', models.PositiveIntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.country')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_team', to='manager.team')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('laps', models.PositiveBigIntegerField()),
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
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='manager.race')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.team')),
            ],
        ),
        migrations.CreateModel(
            name='RaceMechanic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('date_of_birth', models.DateTimeField()),
                ('skill', models.PositiveIntegerField(default=5)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.country')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='race_mechanic', to='manager.team')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.racetrack'),
        ),
        migrations.AddField(
            model_name='race',
            name='teams',
            field=models.ManyToManyField(related_name='races', to='manager.team'),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('races', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='league_races', to='manager.race')),
                ('teams', models.ManyToManyField(blank=True, related_name='league_teams', to='manager.team')),
            ],
        ),
        migrations.CreateModel(
            name='LeadDesigner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('date_of_birth', models.DateTimeField()),
                ('skill', models.PositiveIntegerField(default=5)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.country')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_designer_team', to='manager.team')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Car', max_length=30)),
                ('engine', models.PositiveIntegerField(default=5)),
                ('gearbox', models.PositiveIntegerField(default=5)),
                ('brakes', models.PositiveIntegerField(default=5)),
                ('front_wing', models.PositiveIntegerField(default=5)),
                ('suspension', models.PositiveIntegerField(default=5)),
                ('rear_wing', models.PositiveIntegerField(default=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_owner', to='manager.team')),
            ],
        ),
    ]
