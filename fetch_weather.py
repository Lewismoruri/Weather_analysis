import requests
import json
import pandas as pd
from datetime import datetime, timezone

API_KEY = "800cabfa0fe636c2d4a57271325c7a97"   # <-- replace with your real API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"Error fetching data for {city}: {data.get('message', 'Unknown error')}")
        return None

    weather = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return weather

def save_weather(city, json_file="weather_data.json", csv_file="weather.csv"):
    weather_data = get_weather(city)
    if weather_data:
        # --- JSON ---
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(weather_data)

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        # --- CSV ---
        df = pd.DataFrame(data)   # convert full list to DataFrame
        df.to_csv(csv_file, index=False)

        print(f"✅ Saved weather data for {city}")

if __name__ == "__main__":
    cities = ["Nairobi", "Kisumu", "Mombasa"]
    for city in cities:
        save_weather(city)
