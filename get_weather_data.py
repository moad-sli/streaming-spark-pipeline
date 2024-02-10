import openmeteo_requests
from conf import WEATHER_API_URL
import requests
import pandas as pd

class WeatherApi:
    def __init__(self):
        self.session=requests.session()
        self.weather_api=openmeteo_requests.Client(session=self.session)
        self.meteo=None
        self.params=None

    def init_params(self,latitude,longitude,start_date,end_date,hourly="temperature_2m"):
        self.params={
            "latitude":latitude,
            "longitude":longitude,
            "start_date":start_date,
            "end_date":end_date,
            "hourly":hourly
        }
    def requests_url(self,url):
        self.meteo=self.weather_api.weather_api(url,params=self.params)

class WeatherData:
    def __init__(self,api_response):
        self.responses=api_response
        self.data=None
    def parse_response(self):
        self.data={
            "longitude":self.responses.Longitude(),
            "latitude":self.responses.Latitude(),
            "Elavation":self.responses.Elevation(),
            "Timezone":self.responses.Timezone(),
            "Timezone_abv":self.responses.TimezoneAbbreviation(),
            "hourly":self.responses.Hourly().Variables(0).ValuesAsNumpy()
        }
def main():
    Weather=WeatherApi()
    Weather.init_params(52.52,13.41,"2024-01-25","2024-02-08")
    Weather.requests_url(WEATHER_API_URL)
    for i in Weather.meteo:
        Weather_data=WeatherData(i)
        Weather_data.parse_response()
        print(Weather_data.data)

if __name__=="__main__":
    main()