from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    seats = models.IntegerField(default=0)
    projector = models.BooleanField(default=False)


class RoomReservation(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date')

