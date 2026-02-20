# 🛰️ Project Atlas — Fleet & Route Intelligence Platform

> **Enterprise-grade logistics command center built with Streamlit.**  
> Turn raw delivery data into operational intelligence — optimized zones, live dispatch tracking, and fleet-level insights in a single dark-mode dashboard.

---

[View Live demo](https://atlas-logistics-intelligence.streamlit.app)

## Overview

Project Atlas is an interactive logistics analytics dashboard that simulates real-world fleet operations for a metropolitan delivery network. It uses **K-Means clustering** to automatically group delivery points into optimal truck zones, surfaces key operational metrics at a glance, and provides a full dispatch control interface — all wrapped in a polished, enterprise-quality UI.

Built as a framework for logistics analysts, operations leads, and fleet managers who need fast, visual answers from their delivery data.

---

## Screenshots

```
[ Dashboard Overview ]          [ Dispatch Control Center ]
[ 3D Density Heatmap Map ]      [ Zone Load Distribution ]
```

---

## Features

### 📊 Operational KPIs
Five live metric cards showing total orders, total payload, in-transit count, estimated fuel cost, and fleet efficiency — each with week-over-week deltas.

### 🗺️ Interactive Delivery Map
Switch between two map modes via the sidebar:
- **3D Density Heatmap** — extruded hexagonal columns showing delivery concentration across the metro area, powered by PyDeck.
- **Zone Scatter** — colour-coded scatter plot where each dot represents an order assigned to a specific truck zone.

### ⚡ Automated Zone Optimization
K-Means clustering groups all active delivery points into *N* optimal zones (configurable 2–12 trucks). The algorithm minimises intra-zone travel distance, reducing deadhead miles and fuel overhead. Estimated savings are displayed as a live insight banner.

### 📦 Zone Load Distribution
A visual bar chart showing orders and total payload per truck, colour-coded to flag zones containing critical-priority orders.

### 🕵️ Dispatch Control Center
- Searchable order selector with a live **Dispatch Ticket** card showing: assigned truck/zone, customer, payload weight, ETA, priority badge, status badge, and GPS coordinates.
- **Recent Orders** mini-list with colour-coded priority and status dots for quick visual scanning.

### 🔎 Filtering & Segmentation
Sidebar controls to filter by **Priority Tier** (Critical / High / Medium / Low) and **Delivery Status** (Pending / In-Transit / Delayed) — all downstream views update instantly.

### 📋 Full Order Manifest
Collapsible table showing all 80 orders with every field: ID, customer, priority, status, weight, ETA, coordinates, and assigned zone.

### 📥 Export
One-click CSV download of the current filtered and zone-assigned dispatch schedule directly from the sidebar.

---

## Tech Stack

| Layer | Library |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| Data Manipulation | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| Geospatial Visualisation | [PyDeck](https://deckgl.readthedocs.io/) |
| Machine Learning | [scikit-learn](https://scikit-learn.org/) — K-Means Clustering |
| Fonts | Google Fonts — Syne, DM Sans, DM Mono |

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/project-atlas.git
cd project-atlas

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run atlas_app.py
```

The app will open at `http://localhost:8501`.

### requirements.txt

```
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.26.0
pydeck>=0.9.0
scikit-learn>=1.4.0
```

---

## Usage

| Control | Location | Effect |
|---|---|---|
| Priority Tier filter | Sidebar | Show only selected priority levels |
| Delivery Status filter | Sidebar | Show only selected statuses |
| Active Trucks slider | Sidebar | Set number of K-Means clusters (2–12) |
| Map Mode selector | Sidebar | Switch between 3D Heatmap and Zone Scatter |
| Order ID selector | Dispatch section | Load full dispatch ticket for that order |
| Download button | Sidebar | Export current schedule as CSV |

---

## Project Structure

```
project-atlas/
├── atlas_app.py          # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

As the project grows, a recommended structure for production use would be:

```
project-atlas/
├── app/
│   ├── atlas_app.py      # Main entry point
│   ├── components/       # Reusable UI components
│   ├── logic/            # Optimization & data processing
│   └── styles/           # CSS injection modules
├── data/
│   └── sample_data.csv   # Optional: seed data for demos
├── tests/
├── requirements.txt
├── .streamlit/
│   └── config.toml       # Streamlit theme & server config
└── README.md
```

---

## Configuration

To customise the Streamlit theme and server settings, create `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
backgroundColor = "#080C14"
secondaryBackgroundColor = "#0D1421"
textColor = "#F0F4FF"
font = "sans serif"

[server]
headless = true
port = 8501
```

---

## Connecting Real Data

The app currently generates synthetic data via `load_delivery_data()`. To connect a live data source, replace that function with your own loader:

```python
@st.cache_data(ttl=60)   # refresh every 60 seconds
def load_delivery_data():
    # Example: load from a database, API, or CSV
    return pd.read_csv("s3://your-bucket/deliveries.csv")
    # or: return pd.read_sql("SELECT * FROM orders WHERE date = TODAY", engine)
```

The rest of the app will work without any changes, provided your DataFrame includes the following columns:

| Column | Type | Description |
|---|---|---|
| `order_id` | str | Unique order identifier |
| `lat` | float | Delivery latitude |
| `lon` | float | Delivery longitude |
| `weight_kg` | int/float | Payload weight |
| `priority` | str | `Critical` / `High` / `Medium` / `Low` |
| `delivery_status` | str | `Pending` / `In-Transit` / `Delayed` |
| `eta_minutes` | int | Estimated time to delivery |
| `customer` | str | Customer or client name |

---

## Roadmap

- [ ] Live data ingestion via REST API or WebSocket
- [ ] Haversine-based real road distance calculation
- [ ] Driver assignment and capacity constraint modelling
- [ ] Historical performance trend charts
- [ ] Multi-city / multi-depot support
- [ ] Role-based access (dispatcher vs. executive view)
- [ ] Streamlit Cloud deployment with authentication

---

## Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes, then submit a pull request against the `main` branch.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a pull request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgements

Built on the **Project Atlas Framework v2.0** by **Nexus Tech Analytics**.  
Geospatial rendering powered by [deck.gl](https://deck.gl/) via PyDeck.  
Map tiles by [Mapbox](https://www.mapbox.com/).
