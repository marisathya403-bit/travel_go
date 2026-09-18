"""
URL configuration for travelgo project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views


urlpatterns = [

    path("admin/", admin.site.urls),

    path("accounts/", include("accounts.urls")),

    path("", views.home, name="home"),

    path("destinations/", include("destinations.urls")),

    path(
        "bus-booking/",
        views.bus_booking,
        name="bus_booking"
    ),

    path(
        "hotel-finder/",
        views.hotel_finder,
        name="hotel_finder"
    ),

    path(
        "restaurants/",
        views.restaurants,
        name="restaurants"
    ),

    path(
        "places/",
        views.places_to_visit,
        name="places_to_visit"
    ),

]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )