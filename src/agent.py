import numpy as np


class AstraAgent:

    def __init__(self):

        self.memory = []

        self.service_level = 1.65

        self.inventory_buffer = 1.0

        self.current_strategy = "Balanced"

    # =====================================================
    # OBSERVE SYSTEM STATE
    # =====================================================

    def observe_environment(
        self,
        forecast_error,
        inventory,
        profit
    ):

        state = {

            "forecast_error_mean":
                np.mean(forecast_error),

            "inventory_mean":
                np.mean(inventory),

            "profit_mean":
                np.mean(profit),

            "profit_trend":
                profit[-1] - profit[0]
        }

        return state

    # =====================================================
    # EVALUATE RISK
    # =====================================================

    def evaluate_risk(self, state):

        risk = "LOW"

        if state["forecast_error_mean"] > 35:
            risk = "HIGH"

        elif state["forecast_error_mean"] > 20:
            risk = "MEDIUM"

        return risk

    # =====================================================
    # ADAPT STRATEGY
    # =====================================================

    def adapt_strategy(self, risk):

        reasoning = ""

        if risk == "HIGH":

            self.service_level += 0.15

            self.inventory_buffer += 0.2

            self.current_strategy = "Conservative"

            reasoning = (
                "High forecast volatility detected. "
                "Increasing inventory buffer and "
                "service level to reduce stockout risk."
            )

        elif risk == "MEDIUM":

            self.current_strategy = "Balanced"

            reasoning = (
                "Moderate volatility detected. "
                "Maintaining balanced operational policy."
            )

        else:

            self.service_level -= 0.05

            self.inventory_buffer -= 0.05

            self.current_strategy = "Aggressive"

            reasoning = (
                "Stable demand conditions detected. "
                "Reducing inventory buffer to maximize efficiency."
            )

        return reasoning

    # =====================================================
    # STORE MEMORY
    # =====================================================

    def update_memory(self, state, risk):

        self.memory.append({

            "state": state,

            "risk": risk,

            "strategy": self.current_strategy,

            "service_level": self.service_level,

            "inventory_buffer": self.inventory_buffer
        })

    # =====================================================
    # MAIN AGENT LOOP
    # =====================================================

    def run_agent_cycle(
        self,
        forecast_error,
        inventory,
        profit
    ):

        state = self.observe_environment(
            forecast_error,
            inventory,
            profit
        )

        risk = self.evaluate_risk(state)

        reasoning = self.adapt_strategy(risk)

        self.update_memory(state, risk)

        result = {

            "risk": risk,

            "strategy": self.current_strategy,

            "service_level": round(
                self.service_level,
                2
            ),

            "inventory_buffer": round(
                self.inventory_buffer,
                2
            ),

            "reasoning": reasoning
        }

        return result