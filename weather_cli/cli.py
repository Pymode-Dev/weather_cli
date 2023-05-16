"""
The command line interface
"""

import argparse

from weather_cli.access_api_key import get_api_info
from weather_cli.omeo_weather_api import OmeoDailyForecast
from weather_cli.open_weather_api import OpenWeather

__version__ = get_api_info()["version"]["__version__"]


def parse_args():
    parser = argparse.ArgumentParser(
        prog="weather-cli tools",
        epilog="Thanks for using weather-cli tools",
        description="Check your city weather condition in command line.",
    )

    parser.version = f"weather cli v{__version__}"
    parser.add_argument(
        "--version", "-v", help="Show version of the tool", action="version"
    )

    parser.add_argument("city", type=str, nargs="+", help="Enter your city's name")
    parser.add_argument(
        "--units",
        "-u",
        action="store_true",
        help="Temperature conversion between Celsius and " "Fahrenheit",
    )
    parser.add_argument("-d", "--days", type=int, nargs="?", const=7)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.days:
        omeo_weather = OmeoDailyForecast(args.city, args.days)
        omeo_weather.format_omeoweather_output()
    else:
        open_weather = OpenWeather(args.city, args.units)
        open_weather.format_openweather_output()


if __name__ == "__main__":
    main()
