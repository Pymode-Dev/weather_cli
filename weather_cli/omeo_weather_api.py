"""
The python script that handles api query
"""

import sys
from datetime import datetime
from typing import Final

import requests
from requests import exceptions
from rich.console import Console
from rich.table import Table

from weather_cli.access_api_key import get_api_info

TEMPERATURE_DESCRIPTION_CODE: Final = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "Fog",
    48: "depositing rime fog",
    51: "Drizzle Light Intensity",
    53: "Drizzle Moderate Intensity",
    55: "Drizzle Dense Intensity",
    56: "Freezing Drizzle Light Intensity",
    57: "Freezing Drizzle Dense Intensity",
    61: "Rain Slight Intensity",
    63: "Rain Moderate Intensity",
    65: "Rain Heavy Intensity",
    66: "Freezing Rain Light Intensity",
    67: "Freezing Rain Heavy Intensity",
    71: "Snow Fall Slight Intensity",
    73: "Snow Fall Moderate Intensity",
    75: "Snow fall Heavy Intensity",
    77: "Snow grains",
    80: "Rain Showers Slight Intensity",
    81: "Rain Showers Moderate Intensity",
    82: "Rain Showers Violent Intensity",
    85: "Snow Showers Slight Intensity",
    86: "Snow Showers Heavy Intensity",
    95: "Thunderstorm Slight Intensity",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}

OMEO_URL: str = get_api_info()["omeoweather_api"]["BASE_URl"]
DAILY_URL: str = get_api_info()["geolocation_api"]["BASE_URL"]
API_KEY: str = get_api_info()["openweather_api"]["api_key"]


class OmeoDailyForecast:
    def __init__(self, city_name: list, days=7) -> None:
        self.city: list = city_name
        self.days = days
        self.table = Table()
        self.console = Console()

    def _build_url_for_daily_weather(self) -> str:
        parse_city: str = (
            "+".join(self.city) if len(self.city) > 1 else "".join(self.city)
        )
        api_key: str = f"{API_KEY}"
        final_url: str = f"{DAILY_URL}?q={parse_city}&appid={api_key}"

        return final_url

    def _query_geo_location_api(self) -> list:
        geo_location_url = self._build_url_for_daily_weather()
        return requests.get(f"{geo_location_url}").json()

    def _build_omeo_full_url(self, latitude: float, longitude: float) -> str:
        main_url = (
            f"{OMEO_URL}?latitude={latitude}&longitude={longitude}"
            f"&daily=weathercode,temperature_2m_max&forecast_days="
            f"{self.days}&timezone=auto"
        )
        return main_url

    def query_omeo_weather_api(self) -> dict:
        geo_location_result: dict = self._query_geo_location_api()[0]
        latitude: float = geo_location_result.get("lat")
        longitude: float = geo_location_result.get("lon")
        url_to_query: str = self._build_omeo_full_url(latitude, longitude)
        return requests.get(f"{url_to_query}").json()

    def get_omeoweather_api_result(self) -> dict:
        try:
            forecast_weather_result = self.query_omeo_weather_api()
        except exceptions.ConnectionError:
            self.console.print("No Internet Connection...", style="red")
        else:
            return forecast_weather_result

    def get_date_weathercode_and_temperature(self) -> zip:
        try:
            api_data = self.get_omeoweather_api_result()
            weather_dates = api_data["daily"]["time"]
            weather_codes = api_data["daily"]["weathercode"]
            weather_temperatures = api_data["daily"]["temperature_2m_max"]
        except KeyError:
            self.console.print("Invalid City or Forecasting Days...", style="yellow")
            sys, exit()
        else:
            return zip(weather_dates, weather_codes, weather_temperatures)

    def format_omeoweather_output(self) -> None:
        self.table.add_column("Date", style="yellow")
        self.table.add_column("Temperature", style="blue")
        self.table.add_column("Description", style="green")

        zipped_weather_data = self.get_date_weathercode_and_temperature()

        for dates, weather_code, weather_temp in zipped_weather_data:
            fmt_time = datetime.fromisoformat(dates).strftime("%d %B, %Y")
            temp_description = TEMPERATURE_DESCRIPTION_CODE[weather_code].title()
            self.table.add_row(fmt_time, f"{weather_temp}`C", temp_description)

        self.console.print(self.table)
