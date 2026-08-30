def calculate_reorder_quantity(
    current_inventory,
    forecast
):
    if not forecast:
        return {
            "forecast_7_days": 0,
            "current_inventory": current_inventory,
            "recommended_order": 0
        }

    total_forecast = sum(
        item["predicted_quantity"]
        for item in forecast
    )

    reorder_quantity = max(
        0,
        round(total_forecast - current_inventory)
    )

    return {
        "forecast_7_days": round(total_forecast, 2),
        "current_inventory": current_inventory,
        "recommended_order": reorder_quantity
    }
