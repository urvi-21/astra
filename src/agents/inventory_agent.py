import numpy as np


class InventoryAgent:

    def optimize(
        self,
        inventory
    ):

        avg_inventory = np.mean(inventory)

        min_inventory = np.min(inventory)

        if min_inventory < 250:

            risk = "High"

        elif min_inventory < 400:

            risk = "Medium"

        else:

            risk = "Low"

        return {
            "avg_inventory": avg_inventory,
            "min_inventory": min_inventory,
            "inventory_risk": risk
        }