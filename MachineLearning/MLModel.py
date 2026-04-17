from __future__ import annotations

import math
from pathlib import Path
from typing import Tuple

import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor


def download_market_data(symbol: str = "BTC-USD", start: str = "2014-04-10") -> pd.DataFrame:
    """Download historical market data from Yahoo Finance."""
    start_date = dt.datetime.fromisoformat(start)
    end_date = dt.datetime.now()

    frame = yf.download(symbol, start=start_date, end=end_date, progress=False)
    if frame.empty:
        raise RuntimeError(f"No market data returned for {symbol}.")

    frame = frame.reset_index()
    return frame.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
    )


def create_dataset(dataset: np.ndarray, time_step: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Create sliding-window sequences for supervised learning."""
    if len(dataset) <= time_step:
        raise ValueError("Dataset is too small for the configured time_step.")

    data_x, data_y = [], []
    for i in range(len(dataset) - time_step):
        data_x.append(dataset[i : i + time_step, 0])
        data_y.append(dataset[i + time_step, 0])

    return np.array(data_x), np.array(data_y)


def train_and_evaluate(time_step: int = 20, show_plot: bool = False) -> None:
    """Train the BTC forecasting model and print evaluation metrics."""
    bitcoindf = download_market_data()
    bitcoindf = bitcoindf.ffill()

    closedf = bitcoindf[["date", "close"]].copy()
    closedf = closedf[closedf["date"] > "2014-04-10"]
    if closedf.empty:
        raise RuntimeError("Filtered dataset is empty after date filtering.")

    close_values = closedf[["close"]].to_numpy()
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close = scaler.fit_transform(close_values)

    training_size = int(len(scaled_close) * 0.70)
    train_data = scaled_close[:training_size]
    test_data = scaled_close[training_size:]

    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        objective="reg:squarederror",
    )
    model.fit(X_train, y_train, verbose=False)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = math.sqrt(mean_squared_error(y_test, predictions))

    test_predict = scaler.inverse_transform(predictions.reshape(-1, 1))
    original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))

    last_window = test_data[-time_step:].reshape(1, -1)
    next_day_prediction_scaled = model.predict(last_window).reshape(-1, 1)
    next_day_prediction = scaler.inverse_transform(next_day_prediction_scaled)[0, 0]
    current_price = float(original_ytest[-1, 0])
    decision = "Buy" if next_day_prediction > current_price else "Sell"
    accuracy = (1 - mae / current_price) * 100 if current_price else 0.0

    print(f"Current price: {current_price:.2f}")
    print(f"Predicted price for the next day: {next_day_prediction:.2f}")
    print(f"Decision: {decision}")
    print(f"MAE: {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print(f"Prediction accuracy: {accuracy:.2f}%")

    if show_plot:
        plt.figure(figsize=(14, 7))
        plt.plot(original_ytest, color="blue", label="Actual Prices")
        plt.plot(test_predict, color="red", label="Predicted Prices")
        plt.title("BTC Actual vs Predicted Prices")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    train_and_evaluate(show_plot=False)
