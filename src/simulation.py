import pandas as pd
import numpy as np


class SupplyChainSimulation:

    def __init__(
        self,
        decision_engine,
        initial_inventory=1000
    ):

        self.decision_engine = decision_engine

        self.inventory = initial_inventory

        self.history = []

    def simulate_day(
        self,
        strategy_row,
        demand_std
    ):

        price = strategy_row["price"]

        predicted_demand = (
            strategy_row["predicted_demand"]
        )

        # -----------------------------
        # SIMULATE ACTUAL DEMAND
        # -----------------------------

        actual_demand = np.random.normal(
            predicted_demand,
            demand_std
        )

        actual_demand = max(actual_demand, 0)

        # -----------------------------
        # INVENTORY DECISION
        # -----------------------------

        order_quantity = (
            strategy_row["order_quantity"]
        )

        self.inventory += order_quantity

        # -----------------------------
        # SALES
        # -----------------------------

        actual_sales = min(
            self.inventory,
            actual_demand
        )

        # -----------------------------
        # UPDATE INVENTORY
        # -----------------------------

        self.inventory -= actual_sales

        # -----------------------------
        # REVENUE + COST
        # -----------------------------

        revenue = (
            actual_sales * price
        )

        holding_cost = (
            self.inventory * 0.1
        )

        profit = (
            revenue - holding_cost
        )

        # -----------------------------
        # LOG RESULTS
        # -----------------------------

        result = {
            "price": price,
            "predicted_demand": predicted_demand,
            "actual_demand": actual_demand,
            "sales": actual_sales,
            "remaining_inventory": self.inventory,
            "profit": profit
        }

        self.history.append(result)

        return result

    def run_simulation(
        self,
        best_strategy,
        demand_std,
        days=30
    ):

        for _ in range(days):

            self.simulate_day(
                best_strategy,
                demand_std
            )

        return pd.DataFrame(self.history)