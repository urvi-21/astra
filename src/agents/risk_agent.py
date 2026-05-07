class RiskAgent:

    def evaluate(
        self,
        avg_error,
        inventory_risk
    ):

        if avg_error > 40:

            return "High"

        if inventory_risk == "High":

            return "High"

        if avg_error > 25:

            return "Medium"

        return "Low"