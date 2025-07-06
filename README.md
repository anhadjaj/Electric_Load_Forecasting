⚡ Electric Load Forecasting
==================================
This project focuses on predicting short-term electric load across England and Wales using enriched SCADA data and weather information. The final model achieves:

  • MAPE: 0.71%
  • MASE: 0.260
  → Implies average prediction accuracy of 99.29%, occasionally exceeding 99.85% on individual days.

📊 Dataset
----------------------------
• Raw SCADA Data: 
  https://drive.google.com/file/d/1ABKyShwOpOo4zCg6T_BYoKGUl9t6LqYs/view?usp=drive_link

• Preprocessing Script: 
  All preprocessing, feature engineering, and weather merging are done in `modify_csv.py`.

🌦️ Weather Data Integration
----------------------------
Historical weather data was fetched from Open-Meteo API:

• Coordinates: (52.5, -1.5) — Center of England & Wales
• Hourly features:
  - temperature_2m
  - relative_humidity_2m
  - dew_point_2m
  - wind_speed_10m
  - cloud_cover
  - shortwave_radiation
  - surface_pressure
  - time zone: Europe/London

• Merged with load data using timestamps for multi-modal forecasting.

🔧 Feature Engineering
----------------------------
Final dataset includes 80+ engineered features:

🕓 Time & Seasonality
  - Hour, quarter, weekday, month
  - Fourier terms: daily, weekly, yearly
  - Sinusoidal encodings

📈 Lag & Rolling Features
  - Demand lags: 15 min to 5 days
  - Rolling mean, std, min, max, skew (1–3 days)
  - EWM averages and trend deltas (3h, 6h)

🌧️ Weather Lag Features
  - Weather lags (2, 3, 5 days)
  - Interaction terms: demand × weather

🔁 Flags & Categorical Encodings
  - Peak-hour flag, holiday/weekend flag
  - High-demand and spike detection
  - One-hot hour buckets (e.g., morning, afternoon)

⚙️ Model & Training
----------------------------
• Model: LightGBM Regressor
  - n_estimators = 200
  - max_depth = 15
  - learning_rate = 0.05

• Training Strategy:
  - Time resolution: 15 minutes
  - TimeSeriesSplit (80% train / 20% test)
  - Target variable: england_wales_demand

📈 Evaluation Metrics
----------------------------
| Metric | Description                    | Value   |
|--------|--------------------------------|---------|
| MAPE   | Mean Absolute % Error          | 0.71 %  |
| MASE   | Mean Absolute Scaled Error     | 0.260   |

✅ Outperforms naive 1-step lag model.
✅ Maintains high accuracy during holidays and peaks.

📅 Daily Visualization
----------------------------
Each test day includes:
  - 96 time block predictions vs actuals
  - Holiday flag & annotations
  - Per-day MAPE & MASE computation

🔮 Future Extensions
----------------------------
• Real-time dashboard with live forecasts
• Integration with grid/load balancing systems
• Anomaly detection for holiday/storm loads
• Include solar/wind generation forecasts
