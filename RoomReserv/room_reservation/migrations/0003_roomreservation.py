# Generated by Django 4.1.3 on 2022-12-03 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reservation', '0002_room_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
                ('comment', models.TextField(null=True)),
                ('room_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='room_reservation.room')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]