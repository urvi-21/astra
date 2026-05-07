import numpy as np


class ForecastAgent:

    def analyze(
        self,
        actual_demand,
        predicted_demand
    ):

        forecast_error = np.abs(
            actual_demand - predicted_demand
        )

        avg_error = np.mean(forecast_error)

        volatility = np.std(actual_demand)

        return {
            "forecast_error": forecast_error,
            "avg_error": avg_error,
            "volatility": volatility
        }