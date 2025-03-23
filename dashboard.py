import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

# PostgreSQL connection
# Replace 'mysecretpassword' with your PostgreSQL password
engine = create_engine('postgresql://postgres:StevenTranBlockHead#PostgreSQL@localhost/website_db')

# Load data
sessions = pd.read_sql_query('SELECT * FROM "session"', engine)
section_views = pd.read_sql_query('SELECT * FROM "section_view"', engine)
clicks = pd.read_sql_query('SELECT * FROM "click"', engine)
messages_df = pd.read_sql_query('SELECT * FROM "message"', engine)


# Rename 'id' to 'session_id' for consistency
sessions = sessions.rename(columns={'id': 'session_id'})

# Convert timestamps to datetime
section_views['timestamp'] = pd.to_datetime(section_views['timestamp'], errors='coerce')
clicks['timestamp'] = pd.to_datetime(clicks['timestamp'], errors='coerce')

# Bounce Rate
session_data = sessions.merge(
    section_views.groupby('session_id')['section'].apply(set).rename('sections_viewed'),
    on='session_id', how='left'
).merge(
    clicks.groupby('session_id').size().rename('click_count'),
    on='session_id', how='left'
)
session_data['sections_viewed'] = session_data['sections_viewed'].apply(lambda x: x if isinstance(x, set) else set())
session_data['click_count'] = session_data['click_count'].fillna(0)
session_data['is_bounce'] = (session_data['sections_viewed'] == {'opening'}) & (session_data['click_count'] == 0)
bounce_rate = session_data['is_bounce'].mean() * 100

# Scroll Depth
depth_map = {'opening': 1, 'projects': 2, 'expertise': 3}
session_data['max_depth'] = session_data['sections_viewed'].apply(
    lambda x: max(depth_map.get(s, 0) for s in x) if x else 0
)
depth_counts = session_data['max_depth'].value_counts().sort_index()

# Define elements, display names, and colors
elements = ['about-me', 'spotify_download', 'british-columbia', 'concert-venue', 'github']
display_names = ['About Me', 'Spotify Download', 'British Columbia', 'Concert Venue', 'GitHub']
colors = ['red', 'green', 'skyblue', 'yellow', 'darkgray']

# Section Engagement
clicks_per_element = clicks['element'].value_counts()
counts = [clicks_per_element.get(element, 0) for element in elements]



# Existing code for average time on page
all_timestamps = pd.concat([section_views[['session_id', 'timestamp']], clicks[['session_id', 'timestamp']]])
event_times = all_timestamps.groupby('session_id')['timestamp'].agg(['min', 'max'])
event_times['duration'] = (event_times['max'] - event_times['min']).dt.total_seconds()
average_duration = event_times['duration'].mean()

# Compute average time per section
all_events = pd.concat([section_views[['session_id', 'timestamp']], clicks[['session_id', 'timestamp']]])
last_event_times = all_events.groupby('session_id')['timestamp'].max()
section_views_sorted = section_views.sort_values(['session_id', 'timestamp'])
section_views_sorted['next_view_time'] = section_views_sorted.groupby('session_id')['timestamp'].shift(-1)
section_views_sorted = section_views_sorted.merge(last_event_times.rename('last_event_time'), on='session_id')
section_views_sorted['end_time'] = section_views_sorted['next_view_time'].fillna(section_views_sorted['last_event_time'])
section_views_sorted['duration'] = (section_views_sorted['end_time'] - section_views_sorted['timestamp']).dt.total_seconds()
average_time_per_section = section_views_sorted.groupby('section')['duration'].mean()



#MOBILE 



# Import the Session model from app.py (adjust the import based on your file structure)
from app import Session  # If dashboard.py is in the same directory as app.py


SessionLocal = sessionmaker(bind=engine)

# Query all sessions
db_session = SessionLocal()
sessions = db_session.query(Session).all()
db_session.close()

# Count sessions by device type
device_counts = {'mobile': 0, 'laptop': 0}
for session in sessions:
    if session.device_type == 'mobile':
        device_counts['mobile'] += 1
    elif session.device_type == 'laptop':
        device_counts['laptop'] += 1

# Calculate percentages
total_sessions = len(sessions)
mobile_percentage = (device_counts['mobile'] / total_sessions * 100) if total_sessions > 0 else 0
laptop_percentage = (device_counts['laptop'] / total_sessions * 100) if total_sessions > 0 else 0



# Create grid layout
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns([1, 2])

# Row 1, Column 1: Bounce Rate and Average Time on Page
# Display in Streamlit
with col2:
    st.metric("Bounce Rate", f"{bounce_rate:.2f}%")
    st.metric("Average Time on Page", f"{average_duration:.2f} seconds")
    st.subheader("Average Time per Section")
    for section, avg_time in average_time_per_section.items():
        st.metric(section.capitalize(), f"{avg_time:.2f} seconds")

# Row 1, Column 2: Scroll Depth
with col4:
    st.write("**Scroll Depth (Sections Reached)**")
    st.bar_chart(depth_counts.rename({1: 'Opening', 2: 'Projects', 3: 'Expertise'}))

with col3:
    st.write("**Section Engagement (Clicks)**")
    fig, ax = plt.subplots()
    ax.bar(range(len(elements)), counts, color=colors)
    ax.set_xticks(range(len(elements)))
    ax.set_xticklabels(display_names, rotation=45, ha='right')
    ax.set_xlabel('Elements')
    ax.set_ylabel('Number of Clicks')
    ax.set_title('Clicks by Element')
    st.pyplot(fig)

with col1:
    st.subheader("Total Users")
    st.metric("Count", device_counts['mobile'] + device_counts['laptop'])
    st.subheader("Device Type Distribution")
    st.metric("Mobile", f"{device_counts['mobile']} sessions ({mobile_percentage:.2f}%)")
    st.metric("Laptop", f"{device_counts['laptop']} sessions ({laptop_percentage:.2f}%)")

# Row 2, Columns 2 and 3: Messages Table
with col5:
    st.write("**Messages**")
    st.dataframe(messages_df, height=300)