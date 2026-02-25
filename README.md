# Chicago Community Health Dashboard

An interactive data analytics dashboard visualizing public health indicators across 77 Chicago community areas.

## Demo

<img width="1408" height="797" alt="Screenshot 2026-02-24 at 4 04 52 PM" src="https://github.com/user-attachments/assets/a70fc6dd-b425-4b3d-bb34-1ed608ec5727" />




## Features
- KPI cards showing average, max, and min health indicators
- Top 15 communities bar chart
- Scatter plots with trendlines correlating health indicators with poverty and income
- Poverty rate distribution histogram
- Dropdown to switch between 27 health indicators
- Built on real data from the Chicago Data Portal

## Tech Stack
- Python, Pandas, Plotly Dash
- SQLite (data storage)
- Chicago Data Portal API (SODA)
- Render (deployment)

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 data.py
python3 app.py
```

Open http://127.0.0.1:8050

## Data Source
[Chicago Data Portal - Public Health Statistics](https://data.cityofchicago.org/resource/iqnk-2tcu.json)
