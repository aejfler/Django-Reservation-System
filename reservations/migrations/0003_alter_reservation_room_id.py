# Generated by Django 4.0.5 on 2022-07-02 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.room'),
        ),
    ]
