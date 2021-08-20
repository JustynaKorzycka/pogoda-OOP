import json, os
import requests
import datetime
import os.path

class FileMixin:
  def __init__(self, file_name_):
    self.file_name = file_name_

  def load_data_to_doc(self, record):
    with open(self.file_name, "a+") as file:
      json.dump(record,file)
      file.write(os.linesep)

  def check_and_get_record(self, request_date, city):
    if os.path.exists(self.file_name):
      with open(self.file_name, 'r') as file:
        for line in file:
          if len(line)>1:
            converted_data = json.loads(line)
            if converted_data['location']['name'] == city and request_date in converted_data['location']['localtime']:
              return converted_data
        else:
          return False

class ConectionMixin:
  def __init__(self, api_key_):
    self.url = 'http://api.weatherapi.com/v1/current.json?'
    self.api_key = api_key_

  def connect_with_api(self, city_name):
    payload = {'key': self.api_key, 'q':{city_name}}
    try:
      response = requests.get(self.url, params=payload)
    except requests.exceptions.RequestException as e:
      print(f'Błąd: {e}')
      raise SystemExit(e)
    weather_data = response.json()
    return weather_data

class WeatherAPI:
  def __init__(self, file, api_key):
    self.record = None
    self.file = file
    self.api_key = api_key
  
  def get_data(self, location):
    current_date = str(datetime.date.today())
    self.record = self.file.check_record(current_date, location)
    if not self.record:
      connectionWIthApi =  ConectionMixin(self.api_key)
      self.record = connectionWIthApi.connect_with_api(location)
      if self.record.get('error'):
        print(f'Błąd: {self.record}')
        return 0
      self.file.load_data_to_doc(self.record)
    self.print_weather_data()
  
  def print_weather_data(self):
    city = self.record['location']['name']
    cur_date = self.record['location']['localtime']
    temp = self.record['current']['temp_c']
    humidity = self.record['current']['humidity']
    cloud = self.record['current']['cloud']
    wind_speed = self.record['current']['wind_kph']
    pressure = self.record['current']['pressure_mb']
    # chance_of_rain = self.record['current']['chance_of_rain']
    # chance_of_snow = self.record['current']['chance_of_snow']
    print(f'Miasto: {city}\n Czas: {cur_date} \n Temperatura: {temp}\n Wilgotność powietrza: {humidity}%\n Zachmurzenie: {cloud}% \n Prędkość wiatru: {wind_speed}km/h \n Ciśnienie: {pressure} mbar \n ')

def main():
  api_key = 'c52833b4ef704f9e8f3151342211808'
  file_name = 'weatherData.txt'
  file_manager = FileMixin(file_name)
  weatherData = WeatherAPI(file_manager, api_key)
  while True:
    location = input('Wpisz miasto: ')
    if location == '0':
      break
    weatherData.get_data(location)

if __name__ == '__main__':
  main()
 
