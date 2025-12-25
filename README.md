
# Earthquake Tracker Dashboard

An interactive web application built with **Dash** and **Plotly** to visualize and analyze global seismic activity.  
This project features a statistical dashboard and a high-resolution **3D interactive globe** using the **ETOPO1** topographic model.

---

## Features

- **Global 3D Explorer**  
  Visualize earthquakes on a 3D sphere with realistic relief.

- **Statistical Analytics**  
  Interactive histograms (Magnitude vs. Depth) and time series.

- **Dynamic Filtering**  
  Filter data by date ranges to observe specific seismic trends.

- **High-Resolution Topography**  
  Integration of NOAA's **ETOPO1** model for accurate seafloor and land relief.

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10+**
- **uv** —> an extremely fast Python package and project manager

### Install `uv`

```bash
# MacOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/DataProject.git
cd DataProject
```

### 2. Sync dependencies

```bash
uv sync
```

---

## Data Setup

### 1. Earthquake Data

The application fetches real-time data from the **USGS API**.  
To initialize your local dataset, run:

```bash
uv run python main.py --fetch-data
```

---

### 2. ETOPO1 Topography (Manual Download)

The high-resolution relief file is too large (~890 MB) to be hosted on GitHub.

Steps:

1. Visit the **NOAA ETOPO Global Relief Model** page  
2. Go to the **ETOPO1 "Legacy"** section  
3. Download: `ETOPO1_Ice_g_gdal.grd.gz`  
4. Decompress to obtain: `ETOPO1_Ice_g_gdal.grd`  
5. Place the file here:

```text
data/cleaned/ETOPO1_Ice_g_gdal.grd
```

---

## Running the App

```bash
uv run python main.py
```

Open your browser at:

```
http://127.0.0.1:8050/
```
