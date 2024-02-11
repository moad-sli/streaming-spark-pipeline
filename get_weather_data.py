import openmeteo_requests
from conf import WEATHER_API_URL
import requests
import pandas as pd
import time
import json

class WeatherApi:
    def __init__(self):
        self.session=requests.session()
        self.weather_api=openmeteo_requests.Client(session=self.session)
        self.meteo=None
        self.params=None

    def init_params(self,latitude,longitude,start_date,end_date,hourly=["temperature_2m"]):
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
            "hourly":self.responses.Hourly(),
            "Weather_data":None
        }
    def parse_hourly(self):
        hourly=self.data.get("hourly")
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_rain = hourly.Variables(1).ValuesAsNumpy()
        hourly_snowfall = hourly.Variables(2).ValuesAsNumpy()
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["rain"] = hourly_rain
        hourly_data["snowfall"] = hourly_snowfall
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe.index=hourly_data["date"].astype(str)
        hourly_dataframe.drop("date",axis=1,inplace=True)
        self.data["Weather_date"]=hourly_dataframe.to_dict(orient="index")
        del self.data["hourly"]
def main():
    f=open("data.json","a")
    Weather=WeatherApi()
    Weather.init_params(52.52,13.41,"2024-01-25","2024-02-08",
                        ["temperature_2m", "rain", "snowfall"])
    Weather.requests_url(WEATHER_API_URL)
    for weather_record in Weather.meteo:
        Weather_data=WeatherData(weather_record)
        Weather_data.parse_response()
        Weather_data.parse_hourly()
        f.write(json.dumps(Weather_data.data)+"\n")


if __name__=="__main__":
    main()