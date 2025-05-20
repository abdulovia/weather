from django.contrib.auth.models import User
from django.shortcuts import redirect, render


from .weather_map_service import WeatherMapService
from .models import Locations


def home(request):
    ws = WeatherMapService()

    context = {"weather_data": []}
    if request.user.is_authenticated:
        locations = request.user.locations_set.all()
        location_coords = [
            (loc.id, loc.name, loc.latitude, loc.longitude) for loc in locations
        ]
        weather_data = ws.get_weather_data_threaded(location_coords)
        context["weather_data"] = weather_data
    return render(request, "locations/home.html", context)


def search(request):
    ws = WeatherMapService()

    query = request.GET.get("q", "default")
    locations = ws.get_geolocations(query)
    context = {"query": query, "locations": locations}
    return render(request, "locations/search.html", context)


def add(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        loc_name = request.POST.get("location")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        loc = Locations(name=loc_name, user=user, latitude=lat, longitude=lon)
        loc.save()
    return redirect("locations:home")


def delete(request):
    if request.method == "POST":
        loc_id = request.POST.get("loc_id")
        location = Locations.objects.get(id=loc_id)
        location.delete()
    return redirect("locations:home")
