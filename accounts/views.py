from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Booking, Wishlist
import requests
from django.conf import settings

# ---------------- REGISTER ---------------- #

def register(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill in all the fields."
            )

            return redirect("register")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        request.session["created_username"] = user.username

        return redirect("account_created")

    return render(
        request,
        "accounts/register.html"
    )


# ---------------- ACCOUNT CREATED ---------------- #

def account_created(request):

    username = request.session.get(
        "created_username",
        ""
    )

    return render(
        request,
        "accounts/account_created.html",
        {
            "username": username
        }
    )


# ---------------- LOGIN ---------------- #

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = User.objects.filter(
            username__iexact=username
        ).first()

        if user is not None:
            actual_username = user.username
        else:
            actual_username = username

        user = authenticate(
            request,
            username=actual_username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            if "created_username" in request.session:
                del request.session["created_username"]

            messages.success(
                request,
                "Login successful!"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")

    return render(
        request,
        "accounts/login.html"
    )


# ---------------- LOGOUT ---------------- #

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("login")


# ---------------- FORGOT PASSWORD ---------------- #

def forgot_password(request):

    if request.method == "POST":

        username_or_email = request.POST.get(
            "username",
            ""
        ).strip()

        user = User.objects.filter(
            username__iexact=username_or_email
        ).first()

        if user is None:

            user = User.objects.filter(
                email__iexact=username_or_email
            ).first()

        if user is None:

            messages.error(
                request,
                "Username or email not found."
            )

            return redirect(
                "forgot_password"
            )

        request.session["reset_user_id"] = user.id

        return redirect(
            "reset_password"
        )

    return render(
        request,
        "accounts/forgot_password.html"
    )


# ---------------- RESET PASSWORD ---------------- #

def reset_password(request):

    user_id = request.session.get(
        "reset_user_id"
    )

    if not user_id:

        messages.error(
            request,
            "Please enter your username or email first."
        )

        return redirect(
            "forgot_password"
        )

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User account not found."
        )

        return redirect(
            "forgot_password"
        )

    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "reset_password"
            )

        user.set_password(
            password
        )

        user.save()

        if "reset_user_id" in request.session:

            del request.session[
                "reset_user_id"
            ]

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect(
            "login"
        )

    return render(
        request,
        "accounts/reset_password.html"
    )


# ---------------- HOME ---------------- #

def home(request):

    return render(
        request,
        "home.html"
    )


# ---------------- BUS BOOKING ---------------- #

def bus_booking(request):

    return render(
        request,
        "bus_booking.html"
    )


# ---------------- SEAT SELECTION ---------------- #

def seat_selection(request):

    travel_name = request.GET.get(
        "travel",
        "Sathya Travels"
    )

    destination = request.GET.get(
        "destination",
        "Bangalore"
    )

    passengers = request.GET.get(
        "passengers",
        "1"
    )

    try:

        passengers = int(
            passengers
        )

    except (ValueError, TypeError):

        passengers = 1

    passengers = max(
        1,
        min(passengers, 10)
    )

    # Save travel details in session

    request.session[
        "travel_name"
    ] = travel_name

    request.session[
        "destination"
    ] = destination

    request.session[
        "passengers"
    ] = passengers

    context = {

        "travel_name": travel_name,

        "destination": destination,

        "passengers": passengers,

    }

    return render(
        request,
        "accounts/seat_selection.html",
        context
    )


# ---------------- PASSENGER DETAILS ---------------- #

def passenger_details(request):

    selected_seats = request.GET.get(
        "seats",
        request.POST.get(
            "selected_seats",
            ""
        )
    )

    total_amount = request.GET.get(
        "total",
        request.POST.get(
            "total_amount",
            "0"
        )
    )

    if request.method == "POST":

        passenger_name = request.POST.get(
            "full_name",
            ""
        )

        passenger_age = request.POST.get(
            "age",
            0
        )

        passenger_gender = request.POST.get(
            "gender",
            ""
        )

        mobile_number = request.POST.get(
            "mobile",
            ""
        )

        email = request.POST.get(
            "email",
            ""
        )

        travel_name = request.session.get(
            "travel_name",
            "Sathya Travels"
        )

        destination = request.session.get(
            "destination",
            "Bangalore"
        )

        # User login check

        if not request.user.is_authenticated:

            messages.error(
                request,
                "Please login before booking."
            )

            return redirect(
                "login"
            )

        booking = Booking.objects.create(

            user=request.user,

            travel_name=travel_name,

            destination=destination,

            selected_seats=selected_seats,

            passenger_name=passenger_name,

            passenger_age=passenger_age,

            passenger_gender=passenger_gender,

            mobile_number=mobile_number,

            email=email,

            total_amount=total_amount

        )

        request.session[
            "booking_id"
        ] = booking.id

        return redirect(
            "review_booking"
        )

    context = {

        "selected_seats": selected_seats,

        "total_amount": total_amount,

    }

    return render(
        request,
        "accounts/passenger_details.html",
        context
    )


# ---------------- REVIEW BOOKING ---------------- #

def review_booking(request):

    booking_id = request.session.get(
        "booking_id"
    )

    if not booking_id:

        return redirect(
            "passenger_details"
        )

    try:

        booking = Booking.objects.get(
            id=booking_id
        )

    except Booking.DoesNotExist:

        return redirect(
            "passenger_details"
        )

    context = {

        "booking": booking

    }

    return render(
        request,
        "accounts/review_booking.html",
        context
    )


# ---------------- BOOKING SUCCESS ---------------- #

def booking_success(request):

    booking_id = request.session.get(
        "booking_id"
    )

    if not booking_id:

        return redirect(
            "home"
        )

    try:

        booking = Booking.objects.get(
            id=booking_id
        )

    except Booking.DoesNotExist:

        return redirect(
            "home"
        )

    context = {

        "booking": booking

    }

    return render(
        request,
        "accounts/booking_success.html",
        context
    )


# ---------------- HOTEL FINDER ---------------- #

def hotel_finder(request):

    return render(
        request,
        "accounts/hotel_finder.html"
    )


# ---------------- RESTAURANTS ---------------- #

def restaurants(request):

    return render(
        request,
        "accounts/restaurants.html"
    )

# ---------------- PLACES TO VISIT ---------------- #

def places_to_visit(request):

    destinations = [
{
    "name": "Ooty",
    "image": "/media/destinations/ooty.jpg",
},
{
    "name": "Kodaikanal",
    "image": "/media/destinations/kodaikanal_princess_of_hills.jpg",
},
{
    "name": "Munnar",
    "image": "/media/destinations/Best_places_in_india.jpg",
},
{
    "name": "Bangalore",
    "image": "/media/destinations/BANGALORE.jpg",
},

    ]

    return render(
        request,
        "accounts/places_to_visit.html",
        {
            "destinations": destinations
        }
    )# ---------------- DESTINATION PLACES ---------------- #

def destination_places(request, destination):

    places_data = {

        # ========== OOTY ==========

        "ooty": {

            "name": "Ooty",

            "places": [

                {
                    "name": "Ooty Lake",
                    "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358",
                },

                {
                    "name": "Government Botanical Garden",
                    "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
                },

                {
                    "name": "Doddabetta Peak",
                    "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b",
                },

                {
                    "name": "Pykara Lake",
                    "image": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8",
                },

                {
                    "name": "Rose Garden",
                    "image": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e",
                },

                {
                    "name": "Nilgiri Mountain Railway",
                    "image": "https://images.unsplash.com/photo-1473445361085-b9a07f55608b",
                },

            ]

        },


        # ========== KODAIKANAL ==========

        "kodaikanal": {

            "name": "Kodaikanal",

            "places": [

                {
                    "name": "Kodaikanal Lake",
                    "image": "https://images.unsplash.com/photo-1528127269322-539801943592",
                },

                {
                    "name": "Coaker's Walk",
                    "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7",
                },

                {
                    "name": "Pillar Rocks",
                    "image": "https://images.unsplash.com/photo-1464278533981-50106e6176b1",
                },

                {
                    "name": "Silver Cascade Falls",
                    "image": "https://images.unsplash.com/photo-1433086966358-54859d0ed716",
                },

                {
                    "name": "Bryant Park",
                    "image": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e",
                },

                {
                    "name": "Guna Caves",
                    "image": "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
                },

            ]

        },


        "munnar": {
    "name": "Munnar",
    "places": [
        {
           "name": "Tea Gardens",
           "image": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1200&q=80",
},
        {
            "name": "Mattupetty Dam",
            "image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Eravikulam National Park",
            "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Attukad Waterfalls",
            "image": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Echo Point",
            "image": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Top Station",
            "image": "https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=1200&q=80",
        },
    ]
},

"bangalore": {
    "name": "Bangalore",
    "places": [
        {
            "name": "Bangalore Palace",
            "image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Cubbon Park",
            "image": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Lalbagh Botanical Garden",
            "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Nandi Hills",
            "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "ISKCON Temple",
            "image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Bannerghatta National Park",
            "image": "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=1200&q=80",
        },
    ]
},

        }

    destination = destination.lower()


    data = places_data.get(destination)


    if not data:

        return redirect("places_to_visit")


    return render(

        request,

        "accounts/destination_places.html",

        {

            "destination": data["name"],

            "places": data["places"]

        }

    )
# ---------------- LIVE WEATHER ---------------- #

def weather(request):

    allowed_cities = [
        "Ooty",
        "Kodaikanal",
        "Munnar",
        "Bangalore"
    ]

    city = request.GET.get(
        "city",
        "Ooty"
    )

    # பாதுகாப்பாக allowed destinations மட்டும்
    if city not in allowed_cities:
        city = "Ooty"

    api_key = settings.OPENWEATHER_API_KEY

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    context = {
        "cities": allowed_cities,
        "selected_city": city
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code == 200:

            context.update({
                "city": data["name"],
                "temperature": round(
                    data["main"]["temp"]
                ),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            })

        else:

            context["error"] = (
                "Unable to get weather data."
            )

    except requests.RequestException:

        context["error"] = (
            "Unable to connect to weather service."
        )

    return render(
        request,
        "accounts/weather.html",
        context
    )
    # ---------------- WISHLIST ---------------- #

def wishlist(request):

    if not request.user.is_authenticated:
        return redirect("login")

    items = Wishlist.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(
        request,
        "accounts/wishlist.html",
        {
            "wishlist_items": items
        }
    )


# ---------------- ADD TO WISHLIST ---------------- #

def wishlist_add(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        destination = request.POST.get("destination")
        place_name = request.POST.get("place_name")

        Wishlist.objects.create(
            user=request.user,
            destination=destination,
            place_name=place_name
        )

    return redirect("wishlist")
    # ---------------- REMOVE FROM WISHLIST ---------------- #

def wishlist_remove(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    Wishlist.objects.filter(
        id=item_id,
        user=request.user
    ).delete()

    return redirect("wishlist")