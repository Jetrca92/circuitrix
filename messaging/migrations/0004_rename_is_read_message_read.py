# Generated by Django 4.2.5 on 2024-01-14 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_rename_receiver_message_recipient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='is_read',
            new_name='read',
        ),
    ]
