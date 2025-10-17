# TweeeeeDBT Analytics Dashboard

## Overview
This Streamlit dashboard provides real-time visualization of the IPL tweet analytics pipeline. It connects directly to the PostgreSQL database to display streaming and batch processing results.

## Features

### 📈 Overview Page
- **Real-time metrics**: Total counts of verified tweets, geo-tagged tweets, and team mentions
- **System status**: Health indicators for streaming pipeline and batch processing
- **Data distribution**: Pie chart showing tweet categories

### 🌊 Streaming Analytics Page
- **Geographic distribution**: Bar and pie charts showing tweets by location (Delhi/Mumbai)
- **Team mentions analysis**: Visualization of RCB vs CSK mentions
- **Timeline analysis**: Time-series chart of tweet volume

### ⚖️ Batch vs Stream Comparison Page
- **Performance metrics**: Execution time, CPU usage, and memory consumption
- **Data volume comparison**: Side-by-side comparison of streaming vs batch results
- **Detailed comparison table**: Exact counts and differences

### 📡 Real-time Metrics Page
- **Recent activity**: Latest 10 tweets processed
- **Live statistics**: Total tweets, processing times, data freshness
- **System health**: Overall health score based on various factors

## Usage

1. **Start the dashboard**:
   ```bash
   cd /Users/mayurshadhidhar/Documents/TweeeeeDBT
   streamlit run dashboard.py
   ```

2. **Access the dashboard**: Open http://localhost:8501 in your browser

3. **Navigation**: Use the sidebar to switch between different pages

4. **Auto-refresh**: Enable auto-refresh for live updates every 30 seconds

## Requirements
- PostgreSQL running with data tables populated
- Python packages: streamlit, plotly, psycopg2-binary, pandas
- Database connection configured via `.env` file

## Architecture
```
Dashboard (Streamlit) ← PostgreSQL ← Kafka Consumers ← Spark Streaming ← Kafka Topics
```

The dashboard reads from the same PostgreSQL tables that the Kafka consumers write to, providing real-time insights into the streaming pipeline performance.

## Customization
- **Themes**: Modify `.streamlit/config.toml` for custom colors
- **Refresh rates**: Adjust TTL values in `@st.cache_data` decorators
- **Charts**: Extend with additional Plotly visualizations
- **Metrics**: Add new KPIs by modifying SQL queries

## Troubleshooting
- **Connection errors**: Check PostgreSQL service and credentials in `.env`
- **No data**: Ensure streaming pipeline is running and producing data
- **Performance**: Reduce cache TTL for faster updates or increase for better performance