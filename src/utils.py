import numpy as np


class FeedbackLoopEngine:

    def __init__(
        self,
        inventory_optimizer,
        error_threshold=50
    ):

        self.inventory_optimizer = (
            inventory_optimizer
        )

        self.error_threshold = (
            error_threshold
        )

        self.error_history = []

    def calculate_forecast_error(
        self,
        predicted_demand,
        actual_demand
    ):

        error = abs(
            actual_demand -
            predicted_demand
        )

        self.error_history.append(error)

        return error

    def adjust_inventory_policy(self):

        if len(self.error_history) == 0:
            return

        avg_error = np.mean(
            self.error_history
        )

        # -----------------------------
        # ADAPTIVE POLICY UPDATE
        # -----------------------------

        if avg_error > self.error_threshold:

            self.inventory_optimizer.service_level += 0.1

            print(
                "\n[FEEDBACK LOOP]"
            )

            print(
                "High forecast error detected."
            )

            print(
                "Increasing service level."
            )

        else:

            self.inventory_optimizer.service_level = max(
                1.0,
                self.inventory_optimizer.service_level - 0.05
            )

            print(
                "\n[FEEDBACK LOOP]"
            )

            print(
                "Forecast stable."
            )

            print(
                "Reducing excess inventory risk."
            )

        print(
            f"Updated Service Level: "
            f"{self.inventory_optimizer.service_level:.2f}"
        )