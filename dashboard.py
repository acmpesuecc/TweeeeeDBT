import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'tweedbt'),
    'user': os.getenv('POSTGRES_USER', 'mayurshadhidhar'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

# Page configuration
st.set_page_config(
    page_title="TweeeeeDBT Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

@st.cache_data(ttl=30)
def fetch_data(query):
    """Fetch data from database with caching"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()

def main():
    # Title and header
    st.title("🏏 TweeeeeDBT Analytics Dashboard")
    st.markdown("### Real-time IPL Tweet Analytics")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Streaming Analytics", "Batch vs Stream Comparison", "Real-time Metrics"]
    )
    
    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    if page == "Overview":
        show_overview()
    elif page == "Streaming Analytics":
        show_streaming_analytics()
    elif page == "Batch vs Stream Comparison":
        show_batch_vs_stream()
    elif page == "Real-time Metrics":
        show_realtime_metrics()

def show_overview():
    st.header("📈 System Overview")
    
    # Get basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Streaming metrics
    verified_count = fetch_data("SELECT COUNT(*) as count FROM verified_tweets")
    geo_count = fetch_data("SELECT COUNT(*) as count FROM geo_location")
    team_count = fetch_data("SELECT COUNT(*) as count FROM team_mentions")
    batch_metrics = fetch_data("SELECT * FROM batch_metrics ORDER BY timestamp DESC LIMIT 1")
    
    with col1:
        if not verified_count.empty:
            st.metric("Verified User Tweets", verified_count.iloc[0]['count'])
        else:
            st.metric("Verified User Tweets", "0")
    
    with col2:
        if not geo_count.empty:
            st.metric("Geo-tagged Tweets", geo_count.iloc[0]['count'])
        else:
            st.metric("Geo-tagged Tweets", "0")
    
    with col3:
        if not team_count.empty:
            st.metric("Team Mentions", team_count.iloc[0]['count'])
        else:
            st.metric("Team Mentions", "0")
    
    with col4:
        if not batch_metrics.empty:
            st.metric("Last Batch Time", f"{batch_metrics.iloc[0]['execution_time']:.2f}s")
        else:
            st.metric("Last Batch Time", "N/A")
    
    # System status
    st.subheader("🔧 System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        # Check if data is recent (last 5 minutes)
        recent_data = fetch_data("""
            SELECT COUNT(*) as count FROM verified_tweets 
            WHERE timestamp > NOW() - INTERVAL '5 minutes'
        """)
        
        if not recent_data.empty and recent_data.iloc[0]['count'] > 0:
            st.success("✅ Streaming Pipeline: Active")
        else:
            st.warning("⚠️ Streaming Pipeline: No recent data")
    
    with col2:
        # Check batch processing
        if not batch_metrics.empty:
            last_batch = pd.to_datetime(batch_metrics.iloc[0]['timestamp'])
            time_diff = datetime.now() - last_batch.tz_localize(None)
            if time_diff.total_seconds() < 3600:  # Less than 1 hour
                st.success("✅ Batch Processing: Recent")
            else:
                st.warning("⚠️ Batch Processing: Outdated")
        else:
            st.error("❌ Batch Processing: No data")
    
    # Data distribution chart
    st.subheader("📊 Data Distribution")
    
    # Create pie chart of tweet types
    streaming_data = {
        'Verified Users': verified_count.iloc[0]['count'] if not verified_count.empty else 0,
        'Geo-tagged': geo_count.iloc[0]['count'] if not geo_count.empty else 0,
        'Team Mentions': team_count.iloc[0]['count'] if not team_count.empty else 0
    }
    
    if sum(streaming_data.values()) > 0:
        fig = px.pie(
            values=list(streaming_data.values()),
            names=list(streaming_data.keys()),
            title="Tweet Categories Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for visualization")

def show_streaming_analytics():
    st.header("🌊 Streaming Analytics")
    
    # Geographic distribution
    st.subheader("🗺️ Geographic Distribution")
    geo_data = fetch_data("""
        SELECT location, COUNT(*) as count 
        FROM geo_location 
        GROUP BY location 
        ORDER BY count DESC
    """)
    
    if not geo_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                geo_data, x='location', y='count',
                title="Tweets by Location",
                color='count',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                geo_data, values='count', names='location',
                title="Location Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No geographic data available")
    
    # Team mentions analysis
    st.subheader("🏏 Team Mentions Analysis")
    team_data = fetch_data("""
        SELECT 
            CASE 
                WHEN LOWER(hashtags) LIKE '%rcb%' THEN 'RCB'
                WHEN LOWER(hashtags) LIKE '%csk%' THEN 'CSK'
                ELSE 'Other'
            END as team,
            COUNT(*) as count
        FROM team_mentions 
        GROUP BY team
        ORDER BY count DESC
    """)
    
    if not team_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                team_data, x='team', y='count',
                title="Team Mentions Count",
                color='team',
                color_discrete_map={'RCB': '#FF6B6B', 'CSK': '#FFE66D', 'Other': '#4ECDC4'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Team Stats")
            for _, row in team_data.iterrows():
                st.metric(f"{row['team']} Mentions", row['count'])
    else:
        st.info("No team mention data available")
    
    # Timeline analysis
    st.subheader("⏰ Tweet Timeline")
    timeline_data = fetch_data("""
        SELECT 
            DATE_TRUNC('minute', timestamp) as time_bucket,
            COUNT(*) as tweet_count
        FROM verified_tweets 
        GROUP BY time_bucket 
        ORDER BY time_bucket
    """)
    
    if not timeline_data.empty:
        fig = px.line(
            timeline_data, x='time_bucket', y='tweet_count',
            title="Verified Tweets Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Time", yaxis_title="Tweet Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available")

def show_batch_vs_stream():
    st.header("⚖️ Batch vs Stream Comparison")
    
    # Performance comparison
    st.subheader("🚀 Performance Metrics")
    
    batch_metrics = fetch_data("SELECT * FROM batch_metrics ORDER BY timestamp DESC LIMIT 1")
    
    if not batch_metrics.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Batch Execution Time", 
                f"{batch_metrics.iloc[0]['execution_time']:.3f}s"
            )
        
        with col2:
            st.metric(
                "Batch CPU Usage", 
                f"{batch_metrics.iloc[0]['cpu_percent']:.2f}%"
            )
        
        with col3:
            st.metric(
                "Batch Memory Usage", 
                f"{batch_metrics.iloc[0]['memory_usage_mb']:.2f} MB"
            )
    
    # Data comparison
    st.subheader("📊 Data Volume Comparison")
    
    # Fetch streaming vs batch data counts
    streaming_counts = fetch_data("""
        SELECT 
            'Verified Tweets' as category,
            COUNT(*) as streaming_count
        FROM verified_tweets
        UNION ALL
        SELECT 
            'Geo Tweets' as category,
            COUNT(*) as streaming_count
        FROM geo_location
        UNION ALL
        SELECT 
            'Team Tweets' as category,
            COUNT(*) as streaming_count
        FROM team_mentions
    """)
    
    batch_counts = fetch_data("""
        SELECT 
            'Verified Tweets' as category,
            COUNT(*) as batch_count
        FROM verified_tweets_batch
        UNION ALL
        SELECT 
            'Geo Tweets' as category,
            COUNT(*) as batch_count
        FROM geo_tweets_batch
        UNION ALL
        SELECT 
            'Team Tweets' as category,
            COUNT(*) as batch_count
        FROM team_tweets_batch
    """)
    
    if not streaming_counts.empty and not batch_counts.empty:
        # Merge the data
        comparison_data = pd.merge(streaming_counts, batch_counts, on='category')
        comparison_data = comparison_data.melt(
            id_vars=['category'], 
            value_vars=['streaming_count', 'batch_count'],
            var_name='processing_type',
            value_name='count'
        )
        comparison_data['processing_type'] = comparison_data['processing_type'].str.replace('_count', '')
        
        fig = px.bar(
            comparison_data, x='category', y='count', color='processing_type',
            title="Streaming vs Batch Processing Results",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed comparison table
        st.subheader("📋 Detailed Comparison")
        pivot_data = comparison_data.pivot(index='category', columns='processing_type', values='count')
        pivot_data['Difference'] = pivot_data['streaming'] - pivot_data['batch']
        st.dataframe(pivot_data)
    else:
        st.info("Insufficient data for comparison")

def show_realtime_metrics():
    st.header("📡 Real-time Metrics")
    
    # Recent activity
    st.subheader("🕐 Recent Activity (Last 10 tweets)")
    
    recent_tweets = fetch_data("""
        SELECT * FROM (
            SELECT 
                user_name,
                text,
                timestamp,
                'Verified User' as type
            FROM verified_tweets 
            ORDER BY timestamp DESC 
            LIMIT 5
        ) verified
        
        UNION ALL
        
        SELECT * FROM (
            SELECT 
                user_name,
                text,
                timestamp,
                CONCAT('Geo: ', location) as type
            FROM geo_location 
            ORDER BY timestamp DESC 
            LIMIT 5
        ) geo
        
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    
    if not recent_tweets.empty:
        for _, tweet in recent_tweets.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.write(f"**{tweet['user_name']}**")
                with col2:
                    st.write(tweet['text'][:100] + "..." if len(tweet['text']) > 100 else tweet['text'])
                with col3:
                    st.write(tweet['type'])
                st.divider()
    else:
        st.info("No recent tweets available")
    
    # Live statistics
    st.subheader("📈 Live Statistics")
    
    # Get batch metrics for this section
    batch_metrics = fetch_data("SELECT * FROM batch_metrics ORDER BY timestamp DESC LIMIT 1")
    
    # Create a placeholder for live updates
    placeholder = st.empty()
    
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        
        # Total tweets processed
        total_tweets = fetch_data("""
            SELECT 
                (SELECT COUNT(*) FROM verified_tweets) +
                (SELECT COUNT(*) FROM geo_location) +
                (SELECT COUNT(*) FROM team_mentions) as total
        """)
        
        with col1:
            if not total_tweets.empty:
                st.metric("Total Tweets Processed", total_tweets.iloc[0]['total'])
            else:
                st.metric("Total Tweets Processed", "0")
        
        # Average processing time
        with col2:
            if not batch_metrics.empty:
                st.metric("Avg Batch Time", f"{batch_metrics.iloc[0]['execution_time']:.2f}s")
            else:
                st.metric("Avg Batch Time", "N/A")
        
        # Data freshness
        latest_timestamp = fetch_data("""
            SELECT MAX(timestamp) as latest FROM (
                SELECT timestamp FROM verified_tweets
                UNION ALL
                SELECT timestamp FROM geo_location
                UNION ALL
                SELECT timestamp FROM team_mentions
            ) combined
        """)
        
        with col3:
            if not latest_timestamp.empty and latest_timestamp.iloc[0]['latest']:
                latest = pd.to_datetime(latest_timestamp.iloc[0]['latest'])
                time_diff = datetime.now() - latest.tz_localize(None)
                minutes_ago = int(time_diff.total_seconds() / 60)
                st.metric("Last Update", f"{minutes_ago}m ago")
            else:
                st.metric("Last Update", "N/A")
                minutes_ago = 999  # Default high value
        
        # System health
        with col4:
            health_score = 100  # Start with perfect health
            if minutes_ago > 5:  # No data in last 5 minutes
                health_score -= 30
            if not batch_metrics.empty and batch_metrics.iloc[0]['cpu_percent'] > 80:
                health_score -= 20
            
            if health_score >= 80:
                st.metric("System Health", "🟢 Good", f"{health_score}%")
            elif health_score >= 60:
                st.metric("System Health", "🟡 Fair", f"{health_score}%")
            else:
                st.metric("System Health", "🔴 Poor", f"{health_score}%")

if __name__ == "__main__":
    main()