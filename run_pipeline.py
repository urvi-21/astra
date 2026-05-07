from src.data_preprocessing import load_and_clean_data
from src.feature_engineering import create_features, prepare_data
from src.demand_model import DemandForecastingModel
from src.price_model import PriceElasticityModel
import numpy as np
import pandas as pd
from src.inventory import InventoryOptimizer
from src.decision_engine import DecisionEngine
from src.utils import FeedbackLoopEngine
from src.simulation import SupplyChainSimulation
# -----------------------------
# LOAD + FEATURE ENGINEERING
# -----------------------------

df = load_and_clean_data("data/sales.csv")

df = create_features(df)

X, y = prepare_data(df)

# -----------------------------
# TIME-BASED TRAIN TEST SPLIT
# -----------------------------

split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# -----------------------------
# TRAIN MODEL
# -----------------------------

model = DemandForecastingModel()

model.train(X_train, y_train)

# -----------------------------
# PREDICTIONS
# -----------------------------

predictions = model.predict(X_test)

# -----------------------------
# EVALUATION
# -----------------------------

metrics = model.evaluate(y_test, predictions)

print("\nMODEL PERFORMANCE")
print(metrics)

# -----------------------------
# UNCERTAINTY ESTIMATION
# -----------------------------

mean_pred, std_pred = model.predict_with_uncertainty(X_test.iloc[:5])

print("\nDEMAND FORECAST WITH UNCERTAINTY\n")

for i in range(len(mean_pred)):
    print(
        f"Prediction {i+1}: "
        f"{mean_pred[i]:.2f} ± {std_pred[i]:.2f}"
    )

# -----------------------------
# PRICE ELASTICITY MODEL
# -----------------------------

price_features = [
    'price',
    'month',
    'day_of_week',
    'lag_1',
    'rolling_mean_7'
]

X_price = df[price_features]
y_price = df['sales']

# Time split
X_price_train = X_price.iloc[:split_index]
X_price_test = X_price.iloc[split_index:]

y_price_train = y_price.iloc[:split_index]
y_price_test = y_price.iloc[split_index:]

# Train elasticity model
price_model = PriceElasticityModel()

price_model.train(
    X_price_train,
    y_price_train
)

# -----------------------------
# GENERATE PRICE CURVE
# -----------------------------

sample_features = X_price_test.iloc[[0]].copy()

price_range = np.arange(700, 1200, 50)

curve_df = price_model.generate_price_curve(
    sample_features,
    price_range
)

print("\nPRICE ELASTICITY ANALYSIS\n")

print(curve_df)


# -----------------------------
# INVENTORY OPTIMIZATION
# -----------------------------

inventory_optimizer = InventoryOptimizer()

print("\nINVENTORY OPTIMIZATION\n")

for i in range(len(mean_pred)):

    demand_mean = mean_pred[i]
    demand_std = std_pred[i]

    order_quantity = (
        inventory_optimizer
        .calculate_order_quantity(
            demand_mean,
            demand_std
        )
    )

    risk = (
        inventory_optimizer
        .estimate_stockout_risk(
            demand_mean,
            order_quantity
        )
    )

    print(f"\nForecast {i+1}")

    print(
        f"Demand Forecast: "
        f"{demand_mean:.2f} ± {demand_std:.2f}"
    )

    print(
        f"Recommended Order: "
        f"{order_quantity:.2f}"
    )

    print(
        f"Stockout Risk: {risk}"
    )

# -----------------------------
# DECISION ENGINE
# -----------------------------

decision_engine = DecisionEngine(
    inventory_optimizer
)

# Use uncertainty from first forecast
example_std = std_pred[0]

strategies_df, best_strategy = (
    decision_engine.find_best_strategy(
        curve_df,
        example_std
    )
)

print("\nDECISION ENGINE ANALYSIS\n")

print(strategies_df)

print("\nBEST STRATEGY\n")

print(best_strategy)

# -----------------------------
# SIMULATION ENGINE
# -----------------------------

simulation = SupplyChainSimulation(
    decision_engine
)

simulation_results = (
    simulation.run_simulation(
        best_strategy,
        example_std,
        days=30
    )
)

print("\nSIMULATION RESULTS\n")

print(simulation_results.head())

print("\nTOTAL PROFIT\n")

print(
    simulation_results["profit"].sum()
)

# -----------------------------
# FEEDBACK LOOP
# -----------------------------

feedback_engine = FeedbackLoopEngine(
    inventory_optimizer
)

print("\nFEEDBACK LOOP ANALYSIS\n")

for _, row in simulation_results.iterrows():

    error = (
        feedback_engine
        .calculate_forecast_error(
            row["predicted_demand"],
            row["actual_demand"]
        )
    )

print(
    f"Average Forecast Error: "
    f"{np.mean(feedback_engine.error_history):.2f}"
)

feedback_engine.adjust_inventory_policy()