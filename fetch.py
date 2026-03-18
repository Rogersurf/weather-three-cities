# fetch.py

import requests
import sqlite3
from datetime import date

locations = {
    "Leblon": (-22.985479, -43.222832),
    "Miami Beach": (25.799808, -80.125490),
    "Nørresundby": (57.067962, 9.904931)
}

variables = "temperature_2m_max,precipitation_sum,windspeed_10m_max"

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather (
location TEXT,
forecast_date TEXT,
temperature REAL,
precipitation REAL,
wind REAL
)
""")

for name, (lat, lon) in locations.items():

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily={variables}&timezone=auto"

    r = requests.get(url).json()

    temp = r["daily"]["temperature_2m_max"][1]
    rain = r["daily"]["precipitation_sum"][1]
    wind = r["daily"]["windspeed_10m_max"][1]

    cur.execute(
        "INSERT INTO weather VALUES (?,?,?,?,?)",
        (name, str(date.today()), temp, rain, wind)
    )

conn.commit()
conn.close()

print("Weather data saved")
