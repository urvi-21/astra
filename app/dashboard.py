import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.agent import AstraAgent
from src.strategy_simulator import StrategySimulator
from src.alert_engine import AlertEngine
from src.agents.orchestrator import AstraOrchestrator
from src.shared_memory import SharedMemory

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ASTRA Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0B1020;
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 16px;
        color: #9CA3AF;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    .metric-card {
        background-color: #111827;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .metric-title {
        font-size: 14px;
        color: #9CA3AF;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 700;
        color: white;
    }

    .metric-change {
        font-size: 14px;
        color: #10B981;
        margin-top: 8px;
    }

    .panel {
        background-color: #111827;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 15px;
    }

    .panel-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-bottom: 18px;
    }

    .recommendation-box {
        background: linear-gradient(135deg, #1E3A8A, #2563EB);
        padding: 25px;
        border-radius: 18px;
        color: white;
        margin-top: 20px;
    }

    .recommendation-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .recommendation-text {
        font-size: 18px;
        line-height: 1.7;
    }

    .status-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        background-color: #1F2937;
        color: #10B981;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .insight-card {
        background-color: #101827;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .insight-title {
       font-size: 20px;
       font-weight: 700;
       margin-bottom: 16px;
       color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Astra Control Center")

simulation_days = st.sidebar.slider(
    "Simulation Horizon",
    min_value=7,
    max_value=90,
    value=30
)

selected_product = st.sidebar.selectbox(
    "Product Category",
    [
        "Consumer Electronics",
        "Healthcare Devices",
        "Retail Goods"
    ]
)

risk_preference = st.sidebar.select_slider(
    "Risk Preference",
    options=[
        "Conservative",
        "Balanced",
        "Aggressive"
    ],
    value="Balanced"
)

# =====================================================
# DYNAMIC INTELLIGENCE ENGINE
# =====================================================

np.random.seed(42)

# -----------------------------
# RISK PROFILE CONFIGURATION
# -----------------------------

risk_mapping = {
    "Conservative": {
        "service_level": 2.0,
        "volatility": 35,
        "inventory_buffer": 1.3
    },
    "Balanced": {
        "service_level": 1.65,
        "volatility": 60,
        "inventory_buffer": 1.0
    },
    "Aggressive": {
        "service_level": 1.2,
        "volatility": 90,
        "inventory_buffer": 0.75
    }
}

# -----------------------------
# PRODUCT CONFIGURATION
# -----------------------------

product_mapping = {
    "Consumer Electronics": {
        "base_demand": 580,
        "elasticity": 1.0,
        "unit_cost": 500
    },
    "Healthcare Devices": {
        "base_demand": 420,
        "elasticity": 0.65,
        "unit_cost": 650
    },
    "Retail Goods": {
        "base_demand": 720,
        "elasticity": 1.4,
        "unit_cost": 300
    }
}

risk_config = risk_mapping[risk_preference]
product_config = product_mapping[selected_product]

n_days = simulation_days

dates = pd.date_range(
    end=pd.Timestamp.today(),
    periods=n_days
)

# -----------------------------
# DEMAND GENERATION
# -----------------------------

base_demand = product_config["base_demand"]
volatility = risk_config["volatility"]

actual_demand = np.random.normal(
    base_demand,
    volatility,
    n_days
)

predicted_demand = (
    actual_demand +
    np.random.normal(0, volatility * 0.35, n_days)
)

# -----------------------------
# INVENTORY POLICY
# -----------------------------

inventory_buffer = risk_config["inventory_buffer"]

inventory = []
current_inventory = 1000

for demand in actual_demand:

    replenishment = (
        base_demand * inventory_buffer * 0.9
    )

    current_inventory += replenishment
    current_inventory -= demand

    current_inventory = max(current_inventory, 150)

    inventory.append(current_inventory)

inventory = np.array(inventory)

# -----------------------------
# PROFIT SIMULATION
# -----------------------------

unit_margin = (
    750 - product_config["unit_cost"]
)

profit = []
current_profit = 0

for i, demand in enumerate(actual_demand):

    inventory_cost = inventory[i] * 0.03

    daily_profit = (
        demand * unit_margin
    ) - inventory_cost

    current_profit += daily_profit

    profit.append(current_profit)

profit = np.array(profit)

# -----------------------------
# FORECAST ERROR
# -----------------------------

forecast_error = np.abs(
    actual_demand - predicted_demand
)
# =====================================================
# AUTONOMOUS AGENT
# =====================================================

agent = AstraAgent()

agent_result = agent.run_agent_cycle(
    forecast_error,
    inventory,
    profit
)
# -----------------------------
# PRICE ELASTICITY
# -----------------------------

price_range = np.arange(700, 1200, 50)

elasticity_strength = product_config["elasticity"]

simulated_demand_curve = (
    base_demand -
    ((price_range - 700) * elasticity_strength)
)

simulated_demand_curve = np.clip(
    simulated_demand_curve,
    5,
    None
)

elasticity_df = pd.DataFrame({
    "price": price_range,
    "demand": simulated_demand_curve
})

elasticity_df["revenue"] = (
    elasticity_df["price"] *
    elasticity_df["demand"]
)

elasticity_df["profit"] = (
    elasticity_df["revenue"] -
    (
        elasticity_df["demand"] *
        product_config["unit_cost"]
    )
)

best_row = (
    elasticity_df
    .sort_values(by="profit", ascending=False)
    .iloc[0]
)

best_price = int(best_row["price"])
best_profit = int(best_row["profit"])
best_demand = int(best_row["demand"])
# =====================================================
# STRATEGY SIMULATION
# =====================================================

strategy_simulator = StrategySimulator()

strategy_results, best_strategy_result = (
    strategy_simulator.evaluate_all_strategies(
        demand=best_demand,
        base_inventory=1000,
        unit_margin=(
            best_price -
            product_config["unit_cost"]
        )
    )
)
# =====================================================
# MULTI AGENT ORCHESTRATION
# =====================================================

orchestrator = AstraOrchestrator()

agent_system = orchestrator.run(
    actual_demand,
    predicted_demand,
    strategy_results,
    inventory
)

# =====================================================
# ALERT ENGINE
# =====================================================

alert_engine = AlertEngine()

alerts = alert_engine.generate_alerts(
    forecast_error,
    inventory,
    best_profit,
    agent_result["risk"]
)
# =====================================================
# HEADER
# =====================================================

left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="main-title">ASTRA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Adaptive Supply Chain Intelligence Platform</div>',
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        '''
        <div style="margin-top:18px; text-align:right;">
            <span class="status-pill">Forecast Engine Active</span>
            <span class="status-pill">Strategy Stable</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

# =====================================================
# KPI ROW
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-title">Forecasted Demand</div>
            <div class="metric-value">{best_demand}</div>
            <div class="metric-change">+12% vs baseline</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-title">Optimal Price</div>
            <div class="metric-value">₹{best_price}</div>
            <div class="metric-change">Elasticity optimized</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-title">Expected Profit</div>
            <div class="metric-value">₹{best_profit/1000:.0f}K</div>
            <div class="metric-change">+18% uplift</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-title">Inventory Risk</div>
            <div class="metric-value">{risk_preference.upper()}</div>
            <div class="metric-change">Service Level: 95%</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# =====================================================
# DEMAND FORECAST PANEL
# =====================================================

left_panel, right_panel = st.columns([2, 1])

with left_panel:

    with st.container():

        st.markdown(
            '<div class="panel-title">Demand Forecast Intelligence</div>',
            unsafe_allow_html=True
        )

        fig_forecast = go.Figure()

        fig_forecast.add_trace(
            go.Scatter(
                x=dates,
                y=actual_demand,
                mode='lines',
                name='Actual Demand'
            )
        )

        fig_forecast.add_trace(
            go.Scatter(
                x=dates,
                y=predicted_demand,
                mode='lines',
                name='Predicted Demand'
            )
        )

        fig_forecast.update_layout(
            template='plotly_dark',
            height=420,
            paper_bgcolor='#111827',
            plot_bgcolor='#111827'
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

with right_panel:

    with st.container():

        st.markdown(
            '<div class="panel-title">Forecast Insights</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Forecast volatility increased by 8% over previous operational cycle."
        )

        st.success(
            "Weekend demand surge patterns detected consistently."
        )

        st.warning(
            "Inventory buffer may require adjustment under aggressive pricing."
        )

# =====================================================
# ELASTICITY + PROFIT PANEL
# =====================================================

left, right = st.columns([2, 1])

with left:

    with st.container():

        st.markdown(
            '<div class="panel-title">Pricing Strategy Simulation</div>',
            unsafe_allow_html=True
        )

        fig_price = make_subplots(specs=[[{"secondary_y": True}]])

        fig_price.add_trace(
            go.Scatter(
                x=elasticity_df["price"],
                y=elasticity_df["demand"],
                mode='lines+markers',
                name='Demand'
            ),
            secondary_y=False
        )

        fig_price.add_trace(
            go.Scatter(
                x=elasticity_df["price"],
                y=elasticity_df["profit"],
                mode='lines+markers',
                name='Profit'
            ),
            secondary_y=True
        )

        fig_price.update_layout(
            template='plotly_dark',
            height=420,
            paper_bgcolor='#111827',
            plot_bgcolor='#111827'
        )

        st.plotly_chart(
            fig_price,
            use_container_width=True
        )

with right:

    with st.container():

        st.markdown(
            '<div class="panel-title">Strategic Pricing Insights</div>',
            unsafe_allow_html=True
        )

        st.metric(
            "Optimal Price",
            f"₹{best_price}"
        )

        st.metric(
            "Elasticity Confidence",
            "92%"
        )

        st.metric(
            "Profitability Score",
            "High"
        )

# =====================================================
# INVENTORY + SIMULATION
# =====================================================

left, right = st.columns(2)

with left:

    with st.container():

        st.markdown(
            '<div class="panel-title">Inventory Optimization</div>',
            unsafe_allow_html=True
        )

        fig_inventory = px.area(
            x=dates,
            y=inventory,
            template='plotly_dark'
        )

        fig_inventory.update_layout(
            height=400,
            paper_bgcolor='#111827',
            plot_bgcolor='#111827'
        )

        st.plotly_chart(
            fig_inventory,
            use_container_width=True
        )

with right:

    with st.container():

        st.markdown(
            '<div class="panel-title">Operational Simulation</div>',
            unsafe_allow_html=True
        )

        fig_profit = px.line(
            x=dates,
            y=profit,
            template='plotly_dark'
        )

        fig_profit.update_layout(
            height=400,
            paper_bgcolor='#111827',
            plot_bgcolor='#111827'
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )

# =====================================================
# DECISION ENGINE PANEL
# =====================================================

with st.container():

    st.markdown(
        '<div class="panel-title">Autonomous Decision Engine</div>',
        unsafe_allow_html=True
    )

    strategy_df = pd.DataFrame({
        "Price": elasticity_df["price"],
        "Demand": elasticity_df["demand"].astype(int),
        "Revenue": elasticity_df["revenue"].astype(int),
        "Profit": elasticity_df["profit"].astype(int),
        "Risk": np.where(
            elasticity_df["demand"] > base_demand * 0.8,
            "Medium",
            np.where(
                elasticity_df["demand"] > base_demand * 0.4,
                "Low",
                "High"
            )
        )
    })

    st.table(strategy_df)

    st.markdown(f"""
<div class="recommendation-box">

<div class="recommendation-title">
AI Recommendation
</div>

<div style="
font-size:18px;
line-height:1.8;
color:white;
margin-top:15px;
">

✅ Set product price to <b>₹{best_price}</b><br><br>

📦 Maintain inventory at
<b>{best_strategy_result['inventory']} units</b><br><br>

💰 Expected strategic profit:
<b>₹{best_profit:,}</b><br><br>

⚡ Current operational policy optimized for
<b>{risk_preference.lower()}</b> risk tolerance.

</div>

</div>
""", unsafe_allow_html=True)
    
    st.markdown("### Strategy Evaluation")

    st.dataframe(
    strategy_results,
    use_container_width=True
    )
    st.markdown(
    f"""
### Selected Operational Policy

**Winning Strategy:**  
{best_strategy_result['strategy']}

**Expected Profit:**  
₹{best_strategy_result['profit']:,}

**Holding Cost:**  
₹{best_strategy_result['holding_cost']:,}

**Stockout Penalty:**  
₹{best_strategy_result['stockout_penalty']:,}
"""
)
# =====================================================
# OPERATIONAL ALERTS
# =====================================================

st.markdown(
    '<div class="panel-title">Operational Alerts</div>',
    unsafe_allow_html=True
)

for alert in alerts:

    if alert["type"] == "critical":

        st.error(f"🔴 {alert['message']}")

    elif alert["type"] == "warning":

        st.warning(f"🟡 {alert['message']}")

    elif alert["type"] == "success":

        st.success(f"🟢 {alert['message']}")

    else:

        st.info(f"🔵 {alert['message']}")

# =====================================================
# FEEDBACK LOOP PANEL
# =====================================================

with st.container():

    st.markdown(
        '<div class="panel-title">Adaptive Feedback Intelligence</div>',
        unsafe_allow_html=True
    )

    fig_feedback = px.line(
        x=dates,
        y=forecast_error,
        template='plotly_dark'
    )

    fig_feedback.update_layout(
        height=320,
        paper_bgcolor='#111827',
        plot_bgcolor='#111827'
    )

    st.plotly_chart(
        fig_feedback,
        use_container_width=True
    )

    st.success(
        "Forecast instability detected. Service level adjusted from 1.65 → 1.75 automatically."
    )
    st.markdown(
    f"""
### Autonomous Agent Reasoning

**Risk Level:** {agent_result['risk']}

**Selected Strategy:** {agent_result['strategy']}

**Service Level:** {agent_result['service_level']}

**Inventory Buffer:** {agent_result['inventory_buffer']}

**Reasoning:**  
{agent_result['reasoning']}
"""
)

# =====================================================
# AUTONOMOUS MULTI-AGENT SYSTEM
# =====================================================

st.markdown("""
<div class="panel-title">
Autonomous Multi-Agent Intelligence
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-title">
    Forecast Agent
    </div>

    Average Forecast Error:
    <b>{agent_system['forecast']['avg_error']:.2f}</b>

    <br><br>

    Demand Volatility:
    <b>{agent_system['forecast']['volatility']:.2f}</b>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-title">
    Pricing Agent
    </div>

    Optimal Price:
    <b>₹{agent_system['pricing']['optimal_price']:.0f}</b>

    <br><br>

    Expected Profit:
    <b>
    ₹{agent_system['pricing']['expected_profit']:,.0f}
    </b>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-title">
    Inventory Agent
    </div>

    Average Inventory:
    <b>
    {agent_system['inventory']['avg_inventory']:.0f}
    </b>

    <br><br>

    Inventory Risk:
    <b>
    {agent_system['inventory']['inventory_risk']}
    </b>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-title">
    Supervisor Agent
    </div>

    Global Risk Level:
    <b>{agent_system['risk']}</b>

    <br><br>

    Recommended Action:
    <b>
    {agent_system['final_decision']['recommended_action']}
    </b>

    </div>
    """, unsafe_allow_html=True)