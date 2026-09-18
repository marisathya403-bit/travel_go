from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "account-created/",
        views.account_created,
        name="account_created"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password"
    ),

    path(
        "bus-booking/",
        views.bus_booking,
        name="bus_booking"
    ),

    path(
        "seat-selection/",
        views.seat_selection,
        name="seat_selection"
    ),

    path(
        "passenger-details/",
        views.passenger_details,
        name="passenger_details"
    ),

    path(
        "review-booking/",
        views.review_booking,
        name="review_booking"
    ),

    path(
        "booking-success/",
        views.booking_success,
        name="booking_success"
    ),

    path(
    "places/",
    views.places_to_visit,
    name="places_to_visit"
),

path(
    "places/<str:destination>/",
    views.destination_places,
    name="destination_places"
),
path(
    "weather/",
    views.weather,
    name="weather"
),
path(
    "wishlist/",
    views.wishlist,
    name="wishlist"
),

path(
    "wishlist/add/",
    views.wishlist_add,
    name="wishlist_add"
),
path(
    "wishlist/remove/<int:item_id>/",
    views.wishlist_remove,
    name="wishlist_remove"
),
]