import pandas as pd
import requests
from datetime import timedelta

# === CONFIG ===
input_csv = "historic_demand_2009_2024.csv"
output_csv = "historic_demand_weather_enriched.csv"
lat, lon = 52.5, -1.5
batch_size = 30  # days per API request

# === Load demand data ===
df = pd.read_csv(input_csv)
df["settlement_date"] = pd.to_datetime(df["settlement_date"])
df["timestamp"] = df["settlement_date"] + pd.to_timedelta((df["settlement_period"] - 1) * 15, unit="min")
df = df.set_index("timestamp").sort_index()
all_dates = pd.date_range(df.index.min().normalize(), df.index.max().normalize(), freq="D")

# === Prepare Open-Meteo API ===
hourly_vars = [
    "temperature_2m", "relative_humidity_2m", "dew_point_2m",
    "wind_speed_10m", "cloud_cover", "shortwave_radiation", "surface_pressure"
]
hourly_str = ",".join(hourly_vars)
weather_data = []
success_count = 0

# === Batch Fetching ===
for i in range(0, len(all_dates), batch_size):
    start_date = all_dates[i]
    end_date = min(start_date + timedelta(days=batch_size - 1), all_dates[-1])
    print(f"⏳ Fetching: {start_date.date()} to {end_date.date()} ... ", end="")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": hourly_str,
        "timezone": "UTC"
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        js = r.json()

        timestamps = pd.to_datetime(js["hourly"]["time"])
        for idx in range(len(timestamps)):
            row = {"timestamp": timestamps[idx]}
            for var in hourly_vars:
                row[var] = js["hourly"][var][idx]
            weather_data.append(row)

        print("Success")
        success_count += 1

    except Exception as e:
        print(f"Failed: {e}")

# === Merge and Save ===
if weather_data:
    weather_df = pd.DataFrame(weather_data).set_index("timestamp").sort_index()
    weather_df = weather_df.resample("15T").interpolate("linear")
    merged = df.merge(weather_df, left_index=True, right_index=True, how="left")
    merged.reset_index().to_csv(output_csv, index=False)

    print(f"\n Done! {success_count} batches fetched successfully.")
    print(f"Enriched CSV saved to: {output_csv}")
else:
    print("\n No weather data was fetched. Please check the network/API.")
