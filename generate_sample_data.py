#!/usr/bin/env python3
"""
Sample data generator for TweeeeeDBT dashboard demonstration
"""

import psycopg2
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'tweedbt'),
    'user': os.getenv('POSTGRES_USER', 'mayurshadhidhar'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def generate_sample_data():
    """Generate additional sample data for dashboard demonstration"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Sample data
    users = [
        'cricket_fan_mumbai', 'delhi_sports_lover', 'ipl_enthusiast',
        'rcb_supporter_2024', 'csk_fan_forever', 'mumbai_tweet_guy',
        'verified_sports_user', 'delhi_cricket_news', 'sports_analyst_pro'
    ]
    
    locations = ['Delhi', 'Mumbai', 'New Delhi', 'Mumbai Maharashtra']
    teams = ['RCB', 'CSK']
    
    sample_tweets = [
        "What an incredible match! #IPL2022",
        "Amazing batting performance today #Cricket",
        "Can't believe that catch! #IPL2022",
        "Best match of the season so far",
        "Loving this IPL season #Cricket #IPL2022",
        "That was a spectacular finish!",
        "Great bowling performance #IPL2022",
        "The crowd is going wild! #Cricket"
    ]
    
    print("Generating sample data...")
    
    # Generate verified tweets
    for i in range(5):
        user = random.choice(users)
        text = random.choice(sample_tweets)
        is_verified = random.choice([True, False])
        
        cursor.execute(
            "INSERT INTO verified_tweets (user_name, user_verified, text) VALUES (%s, %s, %s)",
            (user, is_verified, text)
        )
    
    # Generate geo-location tweets
    for i in range(8):
        user = random.choice(users)
        text = random.choice(sample_tweets)
        location = random.choice(locations)
        
        cursor.execute(
            "INSERT INTO geo_location (user_name, text, location) VALUES (%s, %s, %s)",
            (user, text, location)
        )
    
    # Generate team mention tweets
    for i in range(6):
        user = random.choice(users)
        team = random.choice(teams)
        text = f"Go {team}! {random.choice(sample_tweets)} #{team}"
        hashtags = f"[{team}]"
        
        cursor.execute(
            "INSERT INTO team_mentions (user_name, text, hashtags) VALUES (%s, %s, %s)",
            (user, text, hashtags)
        )
    
    # Add a second batch metrics entry
    cursor.execute(
        "INSERT INTO batch_metrics (execution_time, cpu_percent, memory_usage_mb) VALUES (%s, %s, %s)",
        (0.95, 0.72, 98.5)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Sample data generated successfully!")
    print("📊 Dashboard should now show more interesting visualizations")

if __name__ == "__main__":
    generate_sample_data()