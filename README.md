# Earthquake 3D Explorer & Analytics Dashboard

## Project Overview

Our dashboard provides a **multi-dimensional view** of earthquake data by combining:

- A **3D interactive globe**
- A **high-precision 2D map**
- An **analytics dashboard** with statistical insights

The project is built with **Python**, **Dash**, and **Plotly**, and relies on a **hybrid data architecture** that merges large historical datasets with real-time seismic feeds.

---

## Data Strategy & Architecture

### Data Source

All seismic data is sourced from the **USGS (United States Geological Survey) – Earthquake Hazards Program API**.

Each event includes:
- Magnitude
- Depth
- Geographic location
- Timestamp

---

### Storage Optimization — Parquet vs CSV

The application uses **Apache Parquet** instead of CSV for local data persistence, for the following reasons:

1. **High I/O Performance**  
   Parquet is a *columnar* format, enabling faster reads and writes—especially when filtering specific fields. The choice to use Parquet instead of CSV is non-arbitrary and reloading pages is way faster with our huge dataset rather than using CSV format.

2. **Native Type Preservation**  
   Datetime and numeric types are preserved, eliminating repeated parsing operations such as `pd.to_datetime()`.

---

### Hybrid Real-Time Engine

To balance performance and API rate limits, the application uses a **Hybrid Data Loading Strategy**:

- **Historical Data**  
  Long-term seismic data (e.g. last 6 years) loaded from local Parquet cache.
- **Live Data**  
  Lightweight API request fetching only the last 24 hours of events.
- **In-Memory Fusion**  
  Both datasets are merged at runtime to provide historical context alongside real-time updates.

---

## Features

- **3D Explorer**  
  Interactive WebGL globe using NOAA ETOPO1 relief data to visualize seismic depth and global distribution.

- **Global View**  
  2D Mapbox visualization with clustering, paired with a sortable **Ag-Grid** data table.

- **Analytics Module**  
  - Magnitude distribution histograms  
  - Depth vs magnitude scatter plots  
  - Regional seismic activity rankings

- **Performance Optimization**  
  - Server-side caching via **Flask-Caching**
  - Client-side data decimation for smooth rendering of 100k+ points

- **Lazy Loading**  
  Pages and heavy datasets load only when requested, ensuring fast application startup.

---

## Technical Stack

**Frontend / Backend**
- Plotly Dash
- Flask

**Data Processing**
- Pandas
- NumPy
- PyArrow

**Visualization**
- Plotly Graph Objects
- Plotly Express

**UI Components**
- Dash Bootstrap Components
- Dash Ag-Grid

**Caching**
- Flask-Caching (still can be improved with actual filtering)

**HTTP**
- Requests

---

## Installation & Setup

### 1 - Clone the Repository

```bash
git clone <repository-url>
cd DataProject
```

---

### 2 - Environment Setup

This project uses **uv**, a modern and extremely fast Python package manager written in Rust. It automatically handles Python version management (ensuring stability) and dependency resolution.
Since we thrive on being actual modern developers, we decided to use uv for the project instead of a requirements.txt file coupled with pip. As developers we should actually fight having to ever need to write
"source .venv/bin/activate" !

### 1. Install uv
If you don't have `uv` installed:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Setup and run
uv will automatically detect the needed Python version for our project (which is 3.12), create the virtual environment and sync dependencies using the lockfile.
```bash

# Install dependencies (creates .venv based on uv.lock)
uv sync

# Fetch data (Downloads ~6 years of data + ETOPO1 topography if needed)
uv run main.py --fetch-data --start-time 2020-01-01 --end-time 2026-02-01

# Else just launch the app normally
uv run main.py
```
---

### 4 - Data Initialization

Before running the dashboard, fetch historical seismic data from the USGS API.  
The process uses **30-day chunks** to respect API rate limits.

```bash
python main.py --fetch-data --start-time 2020-01-01 --end-time 2026-02-01
```

This will:
- Download raw data
- Clean and normalize events
- Store results in:

```
data/cleaned/cleaned_earthquakes.parquet
```

---

### 5 - Launch the Application

```bash
python main.py
```

The dashboard will be available at:

**http://127.0.0.1:8050**

---

## Project Structure

```plaintext
DataProject/
├── data/
│   ├── cleaned/              # Optimized Parquet datasets
│   └── raw/                  # Raw USGS JSON responses
├── src/
│   ├── components/           # Reusable UI & visualization components
│   │   ├── globe.py
│   │   ├── histogram.py
│   │   ├── seismic_mercator_map.py
│   │   ├── seismic_grid.py
│   │   └── analytics_charts.py
│   │   └── navbar.py
│   ├── pages/                # Dashboard pages
│   │   ├── explorer.py
│   │   ├── analytics.py
│   │   ├── global_view.py
│   │   └── about.py
│   └── utils/
│       ├── data_processor.py # API handling
│       ├── cache_config.py   # Flask-Caching config
│       └── arg_parser.py     # CLI argument management
│       └── etopo_manager.py  # ETOPO management
├── main.py                   # Application entry point
├── pyproject.toml            # Project configuration and dependencies
└── uv.lock                   # Version locking
```

---

## Notes

This project is designed with **scalability and performance** in mind, and can easily be extended to:
- Additional real-time data sources
- Advanced seismic analytics
- Machine learning–based anomaly detection
- Or even creative coding and creative plotting

---

## Made by Yanis Amedjkane & Avishan Abnidezhad
