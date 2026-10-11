# Logistics Data Science — Week 1

Strategic Planning and Data Exploration in Logistics, by Bedi Shivam Jagjeet.

This repository contains the Week 1 Word report and runnable Python illustrations for last-mile logistics data exploration, next-day demand forecasting, and synthetic capacitated routing.

## Problem

A hypothetical e-commerce distributor operates 8 vans, with around 120–200 daily deliveries. It needs to plan demand, allocate vehicles, and reduce travel without exceeding van capacities. These are scenario assumptions, not observed operating statistics.

## KPIs

- On-time delivery rate = on-time completed deliveries / completed deliveries × 100%
- Distance per completed delivery = total fleet km / successful deliveries
- Vehicle capacity utilization = loaded units / vehicle unit capacity × 100%
- Forecast MAE = mean absolute error of actual vs. predicted daily demand
- Fulfillment rate = order lines shipped in full / eligible order lines × 100%

The transaction dataset does **not** have real delivery outcomes or route data. Accordingly, the scripts do not claim measured improvements to on-time delivery or other operations metrics.

## Files

- `report/Week1_Logistics_Strategic_Planning_Report.docx` — completed Week 1 report
- `scripts/explore_orders.py` — reads and cleans the optional UCI retail dataset
- `scripts/demand_forecast.py` — trains regression against a seasonal-naive baseline
- `scripts/route_optimizer.py` — OR-Tools CVRP demo with synthetic stop data
- `data/synthetic_stops.csv` — synthetic planar stops, weights and depot
- `requirements.txt` — dependencies

## Installation

Python 3.10+ recommended:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python scripts/demand_forecast.py
python scripts/route_optimizer.py --input data/synthetic_stops.csv
```

Optional real retail transactions: download Online Retail II from the UCI link below, place the Excel workbook at `data/online_retail_II.xlsx`, then run:

```bash
python scripts/explore_orders.py --input data/online_retail_II.xlsx
python scripts/demand_forecast.py --input data/online_retail_II.xlsx
```

## Data interpretation and limitations

`demand_forecast.py` predicts daily positive **unit quantities**, not daily orders. The UCI dataset provides historical retail invoices and product transactions, **not** actual road networks, delivery locations, route performance or customer delivery windows. Routing uses manually specified synthetic planar coordinates and Euclidean distances, not real kilometers or travel times. All generated results are illustrative; future weeks should use permissioned delivery data and validated road travel-time matrices.

## Research

- [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- [World Bank LPI 2023](https://www.worldbank.org/en/news/press-release/2023/04/21/world-bank-releases-logistics-performance-index-2023)
- [Google OR-Tools vehicle routing](https://developers.google.com/optimization/routing/vrp)
- [Google OR-Tools time windows](https://developers.google.com/optimization/routing/vrptw)
