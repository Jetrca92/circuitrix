# Generated by Django 4.2.5 on 2023-12-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0022_alter_race_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='race',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='race',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
