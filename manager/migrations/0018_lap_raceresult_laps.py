# Generated by Django 4.2.5 on 2023-11-24 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_auto_20231106_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.PositiveIntegerField()),
                ('lap_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='raceresult',
            name='laps',
            field=models.ManyToManyField(blank=True, related_name='lap_race', to='manager.lap'),
        ),
    ]
