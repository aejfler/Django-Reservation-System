from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)

    def reservations_dated(self):
        return self.reservations.order_by('date')


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ("room", "date")
