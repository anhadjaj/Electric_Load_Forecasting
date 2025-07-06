# ⚡ Electric Load Forecasting
This project focuses on predicting short-term electric load across England and Wales using enriched SCADA data and weather information. The final model achieves MAPE: 0.71% and MASE: 0.260, implying an average prediction accuracy of 99.29%, occasionally exceeding 99.85% on individual days.

📊 Dataset
Raw SCADA Data: https://drive.google.com/file/d/1ABKyShwOpOo4zCg6T_BYoKGUl9t6LqYs/view?usp=drive_link

Preprocessing & Enrichment Script: All preprocessing, feature engineering, and weather merging are performed in modify_csv.py.

--> 🌦️ Weather Data Integration
Historical weather data was fetched from the Open-Meteo API using the following parameters:
> Latitude/Longitude: (52.5, -1.5) — Center of England & Wales
> Hourly features added:
  -temperature_2m
  -relative_humidity_2m
  -dew_point_2m
  -wind_speed_10m
  -cloud_cover
  -shortwave_radiation
  -surface_pressure
  -Time zone: Europe/London
> Merged with demand data based on timestamps for robust multi-modal forecasting.

--> Feature Engineering
The final dataset includes over 80+ engineered features, including:

> 🕓 Time & Seasonality
  -Hour, quarter, day of week, month
  -Fourier features (daily, weekly, yearly)
  -Sinusoidal encodings for cyclic time and day-of-year

> Lag & Rolling Features
  -Demand lags: 15 min to 5 days
  -Rolling stats (mean, std, min, max, skew) over 1–3 days
  -Exponential weighted moving averages
  -Trend deltas over 3h and 6h

> 🌧️ Weather Lag Features
  -Weather lags (2, 3, 5 days) for each feature
  -Demand x weather interactions

> Flags & Categorical Encodings
  -Peak-hour flag
  -Holiday/weekend flag
  -High-demand and spike indicators
  -One-hot encoded hour buckets (morning, afternoon, etc.)

> ⚙️ Model & Training
Model Used
  -LightGBM Regressor
  -n_estimators=200
  -max_depth=15
  -learning_rate=0.05

> Training Details
  -15-minute resolution
  -Non-shuffled time-series split (80% train / 20% test)
  -Target: england_wales_demand

> 📈 Evaluation Metrics
Metric	Description	Value
  -MAPE	Mean Absolute Percentage Error	0.71% (Accuracy = 99.29 %)
  -MASE	Mean Absolute Scaled Error (vs naïve)	0.260

> The model substantially outperforms a naive 1-step lag baseline and demonstrates high accuracy even during high-variance periods like holidays and peak demand.

> 📅 Daily Visualization
A random day is sampled from the test set to:
  -Plot actual vs predicted demand (96 time blocks)
  -Highlight if it's a holiday
  -Compute per-day MAPE & MASE

> Future Extensions
  -Real-time prediction dashboard
  -Integration with grid response systems
  -Anomaly detection during holidays or storm periods
  -Incorporation of solar/wind generation capacity data
