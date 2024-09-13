from flask import Flask, jsonify
import requests
import random
import time
from threading import Thread

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = 'e945d7f71eb0e5e621a7dfcce2cb1a43'
CITY_NAME = 'Cape Town'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'

# Global variable for storing solar irradiance
current_irradiance = 800

# Function to retrieve current weather data (temperature)
def get_weather_data(city_name):
    url = BASE_URL.format(city_name, API_KEY)
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return temperature, weather_description
    else:
        return None, None

# Function to simulate solar irradiance based on temperature and weather conditions
def simulate_solar_irradiance(temperature, weather_description):
    global current_irradiance
    base_irradiance = 800
    
    if temperature > 25:
        irradiance = base_irradiance + random.uniform(20, 50)
    elif 15 <= temperature <= 25:
        irradiance = base_irradiance + random.uniform(-20, 20)
    else:
        irradiance = base_irradiance - random.uniform(20, 50)
    
    if 'clear' in weather_description.lower():
        irradiance += random.uniform(50, 100)
    elif 'cloud' in weather_description.lower() or 'overcast' in weather_description.lower():
        irradiance -= random.uniform(100, 200)
    elif 'rain' in weather_description.lower() or 'storm' in weather_description.lower():
        irradiance -= random.uniform(200, 300)
    
    irradiance = max(0, min(irradiance, 1000))
    current_irradiance = irradiance

def update_irradiance():
    while True:
        temperature, weather_description = get_weather_data(CITY_NAME)
        if temperature is not None:
            simulate_solar_irradiance(temperature, weather_description)
        time.sleep(60)  # Update every 60 seconds

@app.route('/api/irradiance', methods=['GET'])
def get_irradiance():
    return jsonify({'irradiance': current_irradiance})

if __name__ == '__main__':
    thread = Thread(target=update_irradiance)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
