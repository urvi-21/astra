from src.agents.forecast_agent import ForecastAgent
from src.agents.pricing_agent import PricingAgent
from src.agents.inventory_agent import InventoryAgent
from src.agents.risk_agent import RiskAgent
from src.agents.supervisor_agent import SupervisorAgent
from src.shared_memory import SharedMemory


class AstraOrchestrator:

    def __init__(self):

        self.forecast_agent = ForecastAgent()

        self.pricing_agent = PricingAgent()

        self.inventory_agent = InventoryAgent()

        self.risk_agent = RiskAgent()

        self.supervisor_agent = SupervisorAgent()

        self.memory = SharedMemory()

    def run(
        self,
        actual_demand,
        predicted_demand,
        strategy_results,
        inventory
    ):

        # ============================================
        # FORECAST AGENT
        # ============================================

        forecast_result = (
            self.forecast_agent.analyze(
                actual_demand,
                predicted_demand
            )
        )

        self.memory.update(
            "forecast_history",
            forecast_result
        )

        # ============================================
        # PRICING AGENT
        # ============================================

        pricing_result = (
            self.pricing_agent.optimize(
                strategy_results
            )
        )

        self.memory.update(
            "pricing_history",
            pricing_result
        )

        # ============================================
        # INVENTORY AGENT
        # ============================================

        inventory_result = (
            self.inventory_agent.optimize(
                inventory
            )
        )

        self.memory.update(
            "inventory_history",
            inventory_result
        )

        # ============================================
        # RISK AGENT
        # ============================================

        risk_result = (
            self.risk_agent.evaluate(
                forecast_result["avg_error"],
                inventory_result["inventory_risk"]
            )
        )

        self.memory.update(
            "risk_history",
            risk_result
        )

        # ============================================
        # AGENT CONFLICT DETECTION
        # ============================================

        conflict = False

        if (
            risk_result == "High"
            and pricing_result["optimal_price"] > 1000
        ):

            conflict = True

        # ============================================
        # AUTONOMOUS SELF-CORRECTION
        # ============================================

        if conflict:

            pricing_result["optimal_price"] -= 100

        # ============================================
        # SUPERVISOR AGENT
        # ============================================

        supervisor_result = (
            self.supervisor_agent.decide(
                risk_result,
                pricing_result["optimal_price"]
            )
        )

        # ============================================
        # FINAL DECISION PACKAGE
        # ============================================

        final_decision = {

            "forecast": forecast_result,

            "pricing": pricing_result,

            "inventory": inventory_result,

            "risk": risk_result,

            "supervisor": supervisor_result,

            "final_decision": {

                "recommended_action":
                supervisor_result["recommended_action"],

                "agent_conflict":
                conflict
            }
        }

        # ============================================
        # STORE FINAL DECISION
        # ============================================

        self.memory.update(
            "decisions",
            final_decision
        )

        return final_decision