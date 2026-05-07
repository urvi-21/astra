from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


class DemandForecastingModel:

    def __init__(self):
        self.model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            random_state=42
        )

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        predictions = self.model.predict(X_test)
        return predictions

    def evaluate(self, y_true, y_pred):

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        return {
            "MAE": mae,
            "RMSE": rmse
        }

    def predict_with_uncertainty(self, X_test, n_simulations=20):

        simulated_predictions = []

        for _ in range(n_simulations):

            noise = np.random.normal(
                0,
                0.01,
                X_test.shape
            )

            noisy_input = X_test + noise

            preds = self.model.predict(noisy_input)

            simulated_predictions.append(preds)

        simulated_predictions = np.array(simulated_predictions)

        mean_prediction = simulated_predictions.mean(axis=0)
        std_prediction = simulated_predictions.std(axis=0)

        return mean_prediction, std_prediction