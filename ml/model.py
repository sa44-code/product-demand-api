from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta


def predict_demand(sales_data):
    if not sales_data:
        return None

    X = np.array(range(len(sales_data))).reshape(-1, 1)

    y = np.array([
        item["quantity_sold"]
        for item in sales_data
    ])

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array(
        range(len(sales_data), len(sales_data) + 7)
    ).reshape(-1, 1)

    predictions = model.predict(future_days)

    # Make sure the last date is a Python date object
    last_date = sales_data[-1]["date"]

    if isinstance(last_date, str):
        last_date = datetime.strptime(
            last_date, "%Y-%m-%d"
        ).date()

    forecast = []

    for i, prediction in enumerate(predictions, start=1):

        forecast_date = last_date + timedelta(days=i)

        forecast.append({
            "date": str(forecast_date),
            "predicted_quantity": round(
                max(0, float(prediction)),
                2
            )
        })

    return forecast
