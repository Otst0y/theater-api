from django.conf import settings
from django.db import models
from django.db.models.functions import Now


class Actor(models.Model):
    first_name = models.CharField(max_length=63, null=False, blank=False)
    last_name = models.CharField(max_length=63, null=False, blank=False)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=63, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=63, null=False, blank=False, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self):
        return self.title


class TheaterHall(models.Model):
    name = models.CharField(max_length=63, null=False, blank=False, unique=True)
    rows = models.PositiveSmallIntegerField()
    seats_in_row = models.PositiveSmallIntegerField()

    @property
    def total_seats(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theater_hall = models.ForeignKey(TheaterHall, on_delete=models.CASCADE, related_name="performances")
    show_time = models.DateTimeField(default=Now)

    def __str__(self):
        return str(self.show_time)


class Ticket(models.Model):
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"Row: {self.row} - Seat: {self.seat}"
