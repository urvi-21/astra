# ASTRA — Autonomous Multi-Agent Supply Chain & Pricing Intelligence Platform

ASTRA is an autonomous AI-powered decision intelligence platform designed to optimize supply chain operations using multi-agent orchestration, machine learning, simulation intelligence, and adaptive operational feedback loops.

The system autonomously analyzes demand forecasts, pricing strategies, inventory risks, and operational uncertainty to recommend profit-maximizing business decisions in real time.


### Live Demo
https://urvi-21-astra-appdashboard-hyquio.streamlit.app/
---

# Problem Statement

Modern supply chain systems operate in highly uncertain environments where fluctuations in customer demand, pricing sensitivity, inventory constraints, and operational risks directly impact profitability.

Traditional analytical systems often:
- operate in silos
- lack adaptive intelligence
- fail to simulate uncertainty
- cannot autonomously coordinate strategic decisions

ASTRA addresses this problem by building a coordinated multi-agent intelligence system capable of autonomous operational reasoning and simulation-driven optimization.

---

# Key Features

## Autonomous Multi-Agent Architecture
ASTRA uses specialized AI agents that independently analyze different operational dimensions while coordinating through a shared memory and orchestration system.

---

## Demand Forecast Intelligence
- Machine learning-based demand forecasting
- Volatility tracking
- Forecast error analysis
- Adaptive operational feedback

---

## Dynamic Pricing Optimization
- Price elasticity simulation
- Revenue optimization
- Profitability analysis
- Strategy evaluation under uncertainty

---

## Inventory Optimization Engine
- Inventory risk analysis
- Stockout prevention
- Service-level balancing
- Operational buffer optimization

---

## Risk-Aware Decision Intelligence
- Operational risk classification
- Strategic conflict detection
- Autonomous self-correction logic
- Risk-adjusted recommendations

---

## Simulation Intelligence
- Multi-scenario operational simulation
- Pricing strategy comparison
- Inventory trade-off analysis
- Profit forecasting under uncertainty

---

## Operational Alert Engine
Real-time operational alerts for:
- inventory instability
- forecast volatility
- aggressive pricing risk
- operational anomalies

---

## Adaptive Feedback Learning
The platform continuously monitors operational performance and dynamically adjusts service-level policies based on changing forecast stability and risk conditions.

---

# Multi-Agent System Design

ASTRA contains specialized autonomous agents:

| Agent | Responsibility |
|---|---|
| Forecast Agent | Forecast error & volatility analysis |
| Pricing Agent | Revenue & pricing optimization |
| Inventory Agent | Inventory planning & stock optimization |
| Risk Agent | Operational risk evaluation |
| Supervisor Agent | Strategic policy coordination |
| Shared Memory Engine | Agent communication & memory persistence |

---

# System Workflow

```text
Demand Data
     ↓
Forecast Agent
     ↓
Pricing Agent
     ↓
Inventory Agent
     ↓
Risk Agent
     ↓
Supervisor Agent
     ↓
Autonomous Strategic Decision
     ↓
Operational Alerts + Feedback Loop
```

---

# Dashboard Capabilities

The Streamlit dashboard provides:

- Real-time forecast intelligence
- Interactive pricing simulation
- Inventory optimization visualization
- Autonomous operational alerts
- Multi-agent reasoning visibility
- Adaptive feedback intelligence
- Strategy evaluation dashboards
- Simulation-driven business analytics

---

# Tech Stack

## Core Technologies
- Python
- Pandas
- NumPy
- Scikit-learn

## Visualization & Dashboard
- Streamlit
- Plotly

## Machine Learning
- Random Forest Regression
- Forecast Error Modeling
- Simulation-Based Decision Systems

## System Architecture
- Multi-Agent Orchestration
- Shared Memory Architecture
- Autonomous Feedback Intelligence

---

# Project Architecture

```text
astra-pricing-engine/
│
├── app/
│   └── dashboard.py
│
├── data/
│
├── src/
│   ├── agents/
│   │   ├── forecast_agent.py
│   │   ├── pricing_agent.py
│   │   ├── inventory_agent.py
│   │   ├── risk_agent.py
│   │   ├── supervisor_agent.py
│   │   └── orchestrator.py
│   │
│   ├── demand_model.py
│   ├── price_model.py
│   ├── inventory.py
│   ├── simulation.py
│   ├── decision_engine.py
│   ├── alert_engine.py
│   ├── strategy_simulator.py
│   └── shared_memory.py
│
├── requirements.txt
├── README.md
└── run_pipeline.py
```

---

# Autonomous Intelligence Features

## Agent Coordination
Agents communicate through a shared orchestration layer and collaboratively generate operational recommendations.

---

## Conflict Resolution
The system autonomously detects strategic conflicts such as:
- aggressive pricing under high risk
- inventory shortages under unstable forecasts

and dynamically self-corrects strategies.

---

## Adaptive Operational Policies
ASTRA continuously adapts operational service levels based on:
- demand volatility
- forecast instability
- inventory pressure
- strategic profitability

---

# Sample Strategic Insights

ASTRA can autonomously recommend:

- reducing inventory buffer during stable demand periods
- increasing service levels under volatility spikes
- adjusting pricing strategies under profitability decline
- balancing risk and operational efficiency dynamically

---

# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/urvi-21/astra.git
cd astra
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Mac/Linux
```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run The Platform

Launch the interactive dashboard:

```bash
streamlit run app/dashboard.py
```

---

# Future Improvements

Planned upgrades include:

- LLM-powered supervisor agents
- Reinforcement learning optimization
- Real-time API integrations
- FastAPI microservices
- PostgreSQL persistence layer
- Docker deployment
- Cloud-native deployment
- Real-time streaming analytics
- Enterprise-scale orchestration

---

# Research & Engineering Focus

This project combines concepts from:

- Artificial Intelligence
- Intelligent Systems
- Multi-Agent Systems
- Decision Intelligence
- Supply Chain Analytics
- Operational Research
- Simulation Engineering
- Adaptive Systems

---

# Author

## Urvi Patel
Biomedical Engineering Student  
AI • Intelligent Systems • Machine Learning • Decision Intelligence

GitHub: https://github.com/urvi-21

---

# License

This project is intended for educational, research, and portfolio purposes.
