#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Weather - OpenWeatherMap</bitbar.title>
# <bitbar.version>v1.0.2</bitbar.version>
# <bitbar.author>Daniel Seripap</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Grabs simple weather information from openweathermap. Needs configuration for location and API key.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

# Alexandre Espinosa Menor: added icon (resized to 30x30 px)
# It needs import Image, os and base64 to work

import json
import urllib2
from random import randint

import base64
from PIL import Image
import os


location = ''
api_key = ''
units = 'metric' # kelvin, metric, imperial
lang = 'en'

def get_wx():

  if api_key == "":
    return False

  try:
    wx = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id=' + location + '&units=' + units + '&lang=' + lang + '&appid=' + api_key + "&v=" + str(randint(0,100))))
  except urllib2.URLError:
    return False

  if units == 'metric':
    unit = 'C'
  elif units == 'imperial':
    unit = 'F'
  else:
    unit = 'K' # Default is kelvin

  try:
    weather_data = {
      'temperature': str(int(round(wx['main']['temp']))),
      'condition': str(wx['weather'][0]['description'].encode('utf-8')),
      'city': wx['name'],
      'unit': '°' + unit,
      'icon': str(wx['weather'][0]['icon']),
    }
  except KeyError:
    return False

  return weather_data

def render_wx():
  weather_data = get_wx()

  if weather_data is False:
    return 'Could not get weather'

  img = save_icon_and_get_encoded(weather_data['icon'])

  # test with real image (at night is just a black dot)
  #img = save_icon_and_get_encoded("10d")

  return weather_data['condition'] + ' ' + weather_data['temperature'] + weather_data['unit'] + "| templateImage="+ img



def save_icon_and_get_encoded(icon):
  url = "http://openweathermap.org/img/wn/" + icon + ".png"

  imgRequest = urllib2.Request(url)
  imgData = urllib2.urlopen(imgRequest).read()

  output = open("/tmp/icon.png",'wb')
  output.write(imgData)
  output.close()

  # resize to 30x30 (images are 50x50, looks too big on my imac)
  img = Image.open('/tmp/icon.png')
  img = img.resize((30, 30), Image.ANTIALIAS)
  img.save('/tmp/icon2.png')


  with open("/tmp/icon2.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

  os.remove("/tmp/icon.png")
  os.remove("/tmp/icon2.png")

  return encoded_string


print render_wx()
