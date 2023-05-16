import sys

import requests
from requests import exceptions
from rich.console import Console
from rich.table import Table

from weather_cli.access_api_key import get_api_info


class OpenWeather:
    API_KEY: str = get_api_info()["openweather_api"]["api_key"]
    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, city_name: list, metrics=False) -> None:
        self.city: list = city_name
        self.metrics: bool = metrics

    def build_url(self) -> str:
        parse_city: str = (
            "+".join(self.city) if len(self.city) > 1 else "".join(self.city)
        )
        api_key: str = f"{self.API_KEY}"
        units: str = "imperial" if self.metrics else "metric"
        url: str = (
            f"{self.BASE_URL}?q={parse_city}&cnt={...}&appid="
            f"{api_key}&units={units}"
        )

        return url

    def queries_api(self) -> dict:
        result = requests.get(self.build_url())
        return result.json()

    def generate_icon(self, weather_id: int) -> str:
        weather_emoji = ""
        if weather_id in range(200, 233):
            weather_emoji = "⛈"
        if weather_id in range(300, 322):
            weather_emoji = ""
        if weather_id in range(500, 532):
            weather_emoji = "🌧"
        if weather_id in range(600, 623):
            weather_emoji = "🌨"
        if weather_id in range(701, 742):
            weather_emoji = "🌫"
        if weather_id in range(781, 782):
            weather_emoji = "🌪"
        if weather_id in range(801, 805):
            weather_emoji = "☁"
        return weather_emoji

    def format_openweather_output(self) -> None:
        table = Table()
        console = Console(emoji=True)

        try:
            api_data: dict = self.queries_api()
            table.add_column("Country, city", style="yellow")
            table.add_column("Temperature", style="blue")
            table.add_column("Description", style="green")
            table.add_column("Icon Description", style="red")
            table.add_row(
                f"{api_data['sys']['country']}, {api_data['name']}",
                f"{api_data['main']['temp']}`{'F' if self.metrics else 'C'}",
                f"{api_data['weather'][0]['description']}".title(),
                self.generate_icon(api_data["weather"][0]["id"]),
            )
            console.print(table)
        except exceptions.ConnectionError:
            console.print("No Internet Connection...", style="red")
            sys.exit()
        except KeyError:
            console.print("City Not Found...", style="red")
