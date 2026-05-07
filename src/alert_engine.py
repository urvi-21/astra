import numpy as np


class AlertEngine:

    def generate_alerts(
        self,
        forecast_error,
        inventory,
        profit,
        risk_level
    ):

        alerts = []

        avg_error = float(np.mean(np.array(forecast_error)))

        min_inventory = float(np.min(np.array(inventory)))

        final_profit = float(np.max(np.array(profit)))

        # Forecast alert
        if avg_error > 35.0:

            alerts.append({
                "type": "critical",
                "message":
                "High forecast volatility detected."
            })

        # Inventory alert
        if min_inventory < 300.0:

            alerts.append({
                "type": "warning",
                "message":
                "Inventory below adaptive threshold."
            })

        # Profit alert
        if final_profit > 140000.0:

            alerts.append({
                "type": "success",
                "message":
                "Pricing strategy outperforming baseline."
            })

        # Agent alert
        alerts.append({
            "type": "info",
            "message":
            f"Autonomous policy updated ({risk_level} risk mode)."
        })

        return alerts