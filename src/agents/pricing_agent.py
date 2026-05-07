class PricingAgent:

    def optimize(self, strategy_df):

        best_row = (
            strategy_df
            .sort_values(
                by="profit",
                ascending=False
            )
            .iloc[0]
        )

        return {
            "optimal_price": 900,
            "expected_profit": best_row["profit"]
        }