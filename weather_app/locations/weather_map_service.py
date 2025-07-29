import concurrent.futures
from django.conf import settings
import requests


class WeatherMapService:
    def get_geolocations(self, query):
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={settings.WEATHER_MAP_TOKEN}"
        response = requests.get(url)
        return response.json()

    def get_weather_data_threaded(self, locations):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.__fetch_weather, loc_id, loc_name, lat, lon)
                for loc_id, loc_name, lat, lon in locations
            ]
            return [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

    def __fetch_weather(self, location_id, location_name, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={settings.WEATHER_MAP_TOKEN}"
        response = requests.get(url)
        weather_data = response.json()

        return {
            "id": location_id,
            "city": location_name,
            "temperature": int(weather_data["main"]["temp"]),
            "condition": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"],
            "humidity": weather_data["main"]["humidity"],
            "image_url": f"https://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png",
        }
