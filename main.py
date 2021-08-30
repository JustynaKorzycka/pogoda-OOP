import json, os
import requests
import datetime
import os.path
import sys

class FileMixin:

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
            converted_date = datetime.datetime.strptime(converted_data['location']['localtime'], "%Y-%m-%d %H:%M")
            if converted_data['location']['name'] == city and request_date == converted_date.date():
              return converted_data
        else:
          return False

class ConectionMixin:

  def connect_with_api(self, location):
    payload = {'key': self.api_key, 'q':{location}}
    try:
      response = requests.get(self.url, params=payload)
    except requests.exceptions.RequestException as e:
      print(f'Błąd: {e}')
      raise SystemExit(e)
    weather_data = response.json()
    return weather_data

class WeatherAPI(FileMixin, ConectionMixin):
  def __init__(self, file_name, api_key):
    self.file_name = file_name
    self.api_key = api_key
    self.url = 'http://api.weatherapi.com/v1/current.json?'
  
  def get_data(self, location):
    current_date = (datetime.date.today())
    self.record = self.check_and_get_record(current_date, location)

    if not self.record:
      self.record = self.connect_with_api(location)
      if self.record.get('error'):
        print(f'Błąd: {self.record}')
        return 
      self.load_data_to_doc(self.record)
    self.print_weather_data()
  
  def print_weather_data(self):
    city = self.record['location']['name']
    cur_date = self.record['location']['localtime']
    temp = self.record['current']['temp_c']
    humidity = self.record['current']['humidity']
    cloud = self.record['current']['cloud']
    wind_speed = self.record['current']['wind_kph']
    pressure = self.record['current']['pressure_mb']
    print(f'Miasto: {city}\n Czas: {cur_date} \n Temperatura: {temp}\n Wilgotność powietrza: {humidity}%\n Zachmurzenie: {cloud}% \n Prędkość wiatru: {wind_speed}km/h \n Ciśnienie: {pressure} mbar \n ')

def main():
  api_key = sys.argv[1]
  file_name = 'weatherData.txt'
  weatherData = WeatherAPI(file_name, api_key)
  while True:
    location = input('Wpisz miasto: ')
    if location == '0':
      break
    weatherData.get_data(location)
    
if __name__ == '__main__':
  main()
 
