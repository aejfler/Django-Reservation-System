# Generated by Django 4.0.5 on 2022-07-03 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_alter_reservation_room_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='room_id',
            new_name='room',
        ),
    ]