
from django.shortcuts import render
from .models import Destination


def destination_list(request):
    destinations = Destination.objects.all().order_by("name")

    return render(
        request,
        "destinations/destination_list.html",
        {
            "destinations": destinations
        }
    )


def home(request):
    destinations = Destination.objects.all().order_by("name")

    return render(
        request,
        "home.html",
        {
            "destinations": destinations
        }
    )