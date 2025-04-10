# Soda Tracker

A simple application to track your soda consumption and visualize your drinking patterns.

## Features

- Track when you drink soda
- View your consumption patterns over time
- Interactive visualizations of your weekly consumption
- Simple and intuitive interface

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Open your browser and navigate to http://localhost:8501
2. Use the interface to log your soda consumption
3. View your consumption patterns in the visualizations section

## Data Storage

All data is stored locally in a SQLite database (`soda_tracker.db`). 