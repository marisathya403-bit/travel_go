from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    travel_name = models.CharField(
        max_length=100
    )

    destination = models.CharField(
        max_length=100
    )

    selected_seats = models.CharField(
        max_length=200
    )

    passenger_name = models.CharField(
        max_length=100
    )

    passenger_age = models.IntegerField()

    passenger_gender = models.CharField(
        max_length=20
    )

    mobile_number = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            self.travel_name +
            " - " +
            self.selected_seats
        )


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    destination = models.CharField(
        max_length=100
    )

    place_name = models.CharField(
        max_length=150
    )

    def __str__(self):

        return (
            self.user.username +
            " - " +
            self.place_name
        )