import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, timezone
from database import SessionLocal, SodaConsumption
from sqlalchemy import func
import calendar
import zoneinfo

# Set timezone for display
LOCAL_TIMEZONE = zoneinfo.ZoneInfo('America/Mexico_City')

st.set_page_config(page_title="Soda Tracker", page_icon="🥤", layout="wide")

st.title("🥤 Soda Consumption Tracker")

# Initialize session state for the database
if 'db' not in st.session_state:
    st.session_state.db = SessionLocal()

# Function to add a new soda consumption entry
def add_soda_consumption():
    db = st.session_state.db
    new_entry = SodaConsumption()
    db.add(new_entry)
    db.commit()
    st.success("Soda consumption logged! 🎉")

# Function to get consumption data
def get_consumption_data():
    db = st.session_state.db
    
    return [
        SodaConsumption(id=entry.id, timestamp=entry.timestamp.replace(tzinfo=timezone.utc))
        for entry in db.query(SodaConsumption).all()
    ]

# Input section
st.header("Log Your Soda Consumption")
if st.button("I just had a soda!"):
    add_soda_consumption()

# Visualization section
st.header("Your Consumption Patterns")

# Get data
consumption_data = get_consumption_data()

if consumption_data:
    # Convert to DataFrame with timezone-aware timestamps
    df = pd.DataFrame([{
        'date': entry.timestamp.astimezone(LOCAL_TIMEZONE).date(),
        'time': entry.timestamp.astimezone(LOCAL_TIMEZONE).time(),
        'datetime': entry.timestamp.astimezone(LOCAL_TIMEZONE)
    } for entry in consumption_data])

    # Calendar-style visualization
    st.subheader("Weekly Calendar View")
    
    # Get the current week's dates
    today = datetime.now(LOCAL_TIMEZONE).date()
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    
    # Create a DataFrame for the week
    week_df = pd.DataFrame({
        'date': week_dates,
        'day_name': [calendar.day_name[date.weekday()] for date in week_dates],
        'date_str': [date.strftime('%Y-%m-%d') for date in week_dates],
        'has_soda': [date in df['date'].values for date in week_dates]
    })
    
    # Define the correct order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create a custom visualization using plotly
    fig_calendar = px.scatter(week_df, x='day_name', y=[1]*7,
                             color='has_soda',
                             color_discrete_map={True: '#FF4B4B', False: '#E0E0E0'},
                             title="This Week's Soda Consumption",
                             labels={'day_name': 'Day', 'y': ''},
                             hover_data=['date_str'],
                             category_orders={'day_name': day_order})
    
    fig_calendar.update_traces(marker=dict(size=20))
    fig_calendar.update_layout(
        yaxis=dict(showticklabels=False, range=[0.5, 1.5]),
        showlegend=False,
        height=200
    )
    st.plotly_chart(fig_calendar, use_container_width=True)
else:
    st.info("No soda consumption data yet. Start tracking by clicking the button above!")