from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0028_alter_championship_season_alter_race_season'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='raceorders',
            constraint=models.UniqueConstraint(fields=('team', 'race'), name='unique_race_order'),
        ),
        migrations.AddConstraint(
            model_name='raceresult',
            constraint=models.UniqueConstraint(fields=('race', 'driver'), name='unique_race_result'),
        ),
    ]
