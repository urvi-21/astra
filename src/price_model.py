from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np


class PriceElasticityModel:

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def train(self, X_train, y_train):

        self.model.fit(X_train, y_train)

    def predict_demand(self, price_df):

        predictions = self.model.predict(price_df)

        return predictions

    def generate_price_curve(
        self,
        base_features,
        price_range
    ):

        results = []

        for price in price_range:

            temp = base_features.copy()

            temp["price"] = price

            predicted_demand = self.model.predict(temp)[0]

            revenue = predicted_demand * price

            results.append({
                "price": price,
                "predicted_demand": predicted_demand,
                "revenue": revenue
            })

        return pd.DataFrame(results)