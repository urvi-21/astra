import pandas as pd
import numpy as np


class DecisionEngine:

    def __init__(
        self,
        inventory_optimizer,
        procurement_cost=500,
        holding_cost_rate=2,
        stockout_penalty_rate=50
    ):

        self.inventory_optimizer = inventory_optimizer

        self.procurement_cost = procurement_cost

        self.holding_cost_rate = holding_cost_rate

        self.stockout_penalty_rate = (
            stockout_penalty_rate
        )

    def evaluate_strategy(
        self,
        price,
        predicted_demand,
        demand_std
    ):

        # -----------------------------
        # INVENTORY DECISION
        # -----------------------------

        order_quantity = (
            self.inventory_optimizer
            .calculate_order_quantity(
                predicted_demand,
                demand_std
            )
        )

        # -----------------------------
        # REVENUE
        # -----------------------------

        revenue = (
            price *
            predicted_demand
        )

        # -----------------------------
        # PROCUREMENT COST
        # -----------------------------

        procurement_cost = (
            order_quantity *
            self.procurement_cost
        )

        # -----------------------------
        # HOLDING COST
        # -----------------------------

        holding_cost = (
            order_quantity *
            self.holding_cost_rate
        )

        # -----------------------------
        # STOCKOUT RISK PENALTY
        # -----------------------------

        expected_stockout = max(
            predicted_demand -
            order_quantity,
            0
        )

        stockout_penalty = (
            expected_stockout *
            self.stockout_penalty_rate
        )

        # -----------------------------
        # FINAL PROFIT
        # -----------------------------

        profit = (
            revenue
            - procurement_cost
            - holding_cost
            - stockout_penalty
        )

        return {
            "price": price,
            "predicted_demand": predicted_demand,
            "order_quantity": order_quantity,
            "revenue": revenue,
            "procurement_cost": procurement_cost,
            "holding_cost": holding_cost,
            "stockout_penalty": stockout_penalty,
            "profit": profit
        }

    def find_best_strategy(
        self,
        price_curve_df,
        demand_std
    ):

        strategies = []

        for _, row in price_curve_df.iterrows():

            strategy = self.evaluate_strategy(
                row["price"],
                row["predicted_demand"],
                demand_std
            )

            strategies.append(strategy)

        strategies_df = pd.DataFrame(strategies)

        best_strategy = (
            strategies_df
            .sort_values(
                by="profit",
                ascending=False
            )
            .iloc[0]
        )

        return strategies_df, best_strategy