from django.contrib import admin
from .models import Booking, Wishlist


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "travel_name",
        "destination",
        "selected_seats",
        "passenger_name",
        "passenger_age",
        "passenger_gender",
        "mobile_number",
        "total_amount",
        "booking_date",
    )

    search_fields = (
        "user__username",
        "travel_name",
        "destination",
        "passenger_name",
        "mobile_number",
    )

    list_filter = (
        "destination",
        "passenger_gender",
        "booking_date",
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "destination",
        "place_name",
    )

    search_fields = (
        "user__username",
        "destination",
        "place_name",
    )

    list_filter = (
        "destination",
    )


# TravelGo Admin Branding

admin.site.site_header = "TravelGo Administration"
admin.site.site_title = "TravelGo Admin"
admin.site.index_title = "Welcome to TravelGo Admin Dashboard"