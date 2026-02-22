import requests  # pyright: ignore[reportMissingModuleSource]
from geopy.distance import geodesic  # pyright: ignore[reportMissingImports]
from datetime import datetime

USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

def get_recent_quakes():
    try:
        response = requests.get(USGS_FEED_URL, timeout=10)
        response.raise_for_status()  # raise error if bad response
        data = response.json()
        print(f"✅ Fetched {len(data['features'])} recent earthquakes")  # Debug print
        return data["features"]
    except Exception as e:
        print(f"❌ Error fetching earthquake data: {e}")
        return []  # return empty list if error

def format_time(epoch_ms):
    """Convert USGS epoch time (ms) to readable string."""
    return datetime.utcfromtimestamp(epoch_ms / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")

def check_threat(user_location, radius_km=500):
    quakes = get_recent_quakes()
    alerts = []

    for quake in quakes:
        try:
            coords = quake["geometry"]["coordinates"]  # [lon, lat, depth]
            quake_location = (coords[1], coords[0])
            distance = geodesic(user_location, quake_location).km
            magnitude = quake["properties"]["mag"]
            place = quake["properties"]["place"]
            time_str = format_time(quake["properties"]["time"])

            print(f"🔎 Checking quake at {place} | Mag: {magnitude} | Dist: {distance:.2f} km")  # Debug

            if distance <= radius_km and magnitude >= 4.5:
                alerts.append({
                    "place": place,
                    "magnitude": magnitude,
                    "distance_km": round(distance, 2),
                    "time": time_str
                })
        except Exception as e:
            print(f"⚠️ Error parsing quake data: {e}")

    print(f"🚨 Alerts found: {len(alerts)}")  # Debug print
    return alerts
