import numpy as np
import pandas as pd


class StrategySimulator:

    def __init__(self):

        self.strategies = {

            "Conservative": {
                "service_level": 2.0,
                "inventory_buffer": 1.3
            },

            "Balanced": {
                "service_level": 1.65,
                "inventory_buffer": 1.0
            },

            "Aggressive": {
                "service_level": 1.2,
                "inventory_buffer": 0.75
            }
        }

    # =====================================================
    # SIMULATE STRATEGY
    # =====================================================

    def simulate_strategy(
        self,
        strategy_name,
        demand,
        base_inventory,
        unit_margin
    ):

        config = self.strategies[strategy_name]

        inventory_buffer = config["inventory_buffer"]

        inventory = (
            base_inventory * inventory_buffer
        )

        stockout_penalty = 0

        if demand > inventory:

            stockout_penalty = (
                demand - inventory
            ) * 120

        revenue = demand * unit_margin

        holding_cost = inventory * 3

        profit = (
            revenue
            - holding_cost
            - stockout_penalty
        )

        result = {

            "strategy": strategy_name,

            "inventory": round(inventory),

            "revenue": round(revenue),

            "holding_cost": round(holding_cost),

            "stockout_penalty": round(stockout_penalty),

            "profit": round(profit)
        }

        return result

    # =====================================================
    # EVALUATE ALL STRATEGIES
    # =====================================================

    def evaluate_all_strategies(
        self,
        demand,
        base_inventory,
        unit_margin
    ):

        results = []

        for strategy in self.strategies:

            result = self.simulate_strategy(
                strategy,
                demand,
                base_inventory,
                unit_margin
            )

            results.append(result)

        results_df = pd.DataFrame(results)

        best_strategy = (
            results_df
            .sort_values(
                by="profit",
                ascending=False
            )
            .iloc[0]
        )

        return results_df, best_strategy