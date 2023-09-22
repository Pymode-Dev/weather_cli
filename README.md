# Weather CLI in the Command Line.

## Check the weather condition of your city.

## Features available are:

- Check the weather condition of your city.
- Word description and Emoji description are available.
- Check the forecasted weather condition of your city upto 16 days ahead.

## Future Features to Add:
- Outfit Recommendation using chatgpt

## API configuration Setting
- Create a file name: secrets.ini.
- Get your Openweather API key.
File template:
"""

; secrets.ini

[version]

__version__=0.2.0

[openweather_api]

api_key=YOUR API KEY

[omeoweather_api]

BASE_URL=https://api.open-meteo.com/v1/forecast

[geolocation_api]

BASE_URL=http://api.openweathermap.org/geo/1.0/direct

"""
Note: Don't put spac in the real file.

## Turn the Repo to a Tool in Linux
- Clone the remote repo.
- Write a bash script that point to the cloning repo path.
- And add this: poetry run weather $1 $2 $3
- Change it to executable file with: chmod u+x [bash script file].
- Move the bash script to /usr/bin so that you will be able to run from anywhere
in the terminal.
- Enjoy Using the tool.

## Feel Free to Contribute
Contact Me:
[Twitter](https://twitter.com/PymodeD)
[Discord]()
