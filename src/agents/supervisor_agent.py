class SupervisorAgent:

    def decide(
        self,
        risk_level,
        optimal_price
    ):

        if risk_level == "High":

            action = (
                "Increase inventory buffers "
                "and stabilize pricing."
            )

        elif risk_level == "Medium":

            action = (
                "Maintain balanced inventory "
                "and pricing strategy."
            )

        else:

            action = (
                "Aggressively optimize profit "
                "through lean inventory."
            )

        return {
            "risk_level": risk_level,
            "recommended_action": action,
            "recommended_price": optimal_price
        }