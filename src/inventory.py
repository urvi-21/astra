import numpy as np


class InventoryOptimizer:

    def __init__(
        self,
        service_level=1.65
    ):

        # Higher service level =
        # more safety stock
        self.service_level = service_level

    def calculate_order_quantity(
        self,
        demand_mean,
        demand_std
    ):

        order_quantity = (
            demand_mean +
            self.service_level * demand_std
        )

        return max(order_quantity, 0)

    def estimate_stockout_risk(
        self,
        demand_mean,
        order_quantity
    ):

        if order_quantity >= demand_mean:
            return "Low"

        elif order_quantity >= 0.8 * demand_mean:
            return "Medium"

        else:
            return "High"