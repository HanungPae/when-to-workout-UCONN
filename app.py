import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set up the page
st.set_page_config(page_title="UConn Gym Tracker", layout="centered")
st.title("🏋️‍♂️ UConn Rec Center Live Occupancy")

# 2. Fetch the live data from your public repo
# IMPORTANT: Replace 'YOUR-USERNAME' with your actual GitHub username!
url = "https://raw.githubusercontent.com/HanungPae/when-to-workout-UCONN/main/data.csv"

# The @st.cache_data(ttl=300) tells the app to fetch fresh data every 5 minutes
@st.cache_data(ttl=300)
def load_data():
    # Read the CSV from GitHub
    df = pd.read_csv(url)
    
    # Convert the raw text timestamp into a readable date/time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Optional but highly recommended: Convert UTC time to UConn's local time (EST)
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    
    return df

df = load_data()

# 3. Create the interactive graph
if not df.empty:
    # Show the very latest percentage in a big, easy-to-read metric
    latest_percent = df.iloc[-1]['percent']
    st.metric(label="Current Occupancy", value=f"{latest_percent}%")

    # Build the interactive line chart
    fig = px.line(
        df, 
        x="timestamp", 
        y="percent", 
        labels={"timestamp": "Time", "percent": "Occupancy (%)"},
        markers=True # Adds little dots to the line, making them easy to tap on your phone
    )
    
    # Clean up the hover pop-up text
    fig.update_traces(hovertemplate='<b>Time:</b> %{x}<br><b>Occupancy:</b> %{y}%<extra></extra>')
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("Waiting for the GitHub Action to collect the first batch of data...")
