#!/bin/bash

# TweeeeeDBT Pipeline Runner
# This script helps run the entire streaming pipeline

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 TweeeeeDBT Pipeline Runner"
echo "================================"

# Function to check if service is running
check_service() {
    local service_name=$1
    local port=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ $service_name is running on port $port"
        return 0
    else
        echo "❌ $service_name is not running on port $port"
        return 1
    fi
}

# Function to start Docker services
start_docker() {
    echo "🐳 Starting Docker services..."
    if docker compose up -d; then
        echo "✅ Docker services started"
        sleep 10  # Wait for services to initialize
    else
        echo "❌ Failed to start Docker services"
        exit 1
    fi
}

# Function to check dependencies
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python3 found: $(python3 --version)"
    else
        echo "❌ Python3 not found"
        exit 1
    fi
    
    # Check Spark
    if command -v spark-submit &> /dev/null; then
        echo "✅ Spark found"
    else
        echo "❌ Spark not found. Please install Apache Spark"
        exit 1
    fi
    
    # Check Docker
    if command -v docker &> /dev/null; then
        echo "✅ Docker found"
    else
        echo "❌ Docker not found. Please install Docker"
        exit 1
    fi
    
    # Check PostgreSQL
    if command -v psql &> /dev/null; then
        echo "✅ PostgreSQL client found"
    else
        echo "⚠️  PostgreSQL client not found. Database operations may fail"
    fi
}

# Function to install Python packages
install_packages() {
    echo "📦 Installing Python packages..."
    if pip3 install -r "docs/Requirement Specification/requirements.txt"; then
        echo "✅ Python packages installed"
    else
        echo "❌ Failed to install Python packages"
        exit 1
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1. 🏗️  Setup & Install Dependencies"
    echo "2. 🐳 Start Docker Services"
    echo "3. ⚡ Start Stream Processing"
    echo "4. 🔄 Start All Consumers"
    echo "5. 📡 Start Producer"
    echo "6. 📊 Start Dashboard"
    echo "7. 🚀 Run Complete Pipeline"
    echo "8. 🧹 Reset Kafka Topics"
    echo "9. 📋 Check Service Status"
    echo "0. ❌ Exit"
    echo ""
}

# Execute choice
case "${1:-menu}" in
    "setup"|"1")
        check_dependencies
        install_packages
        echo "✅ Setup complete!"
        ;;
    "docker"|"2")
        start_docker
        ;;
    "stream"|"3")
        echo "⚡ Starting Stream Processing..."
        cd src/stream_processing
        spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 stream_processing.py &
        echo "✅ Stream Processing started in background"
        ;;
    "consumers"|"4")
        echo "🔄 Starting All Consumers..."
        cd src/consumers
        python3 consumer_geolocation.py &
        python3 consumer_teammentions.py &
        python3 consumer_userverify.py &
        python3 consumer_verifieduserwindowed.py &
        echo "✅ All consumers started in background"
        ;;
    "producer"|"5")
        echo "📡 Starting Producer..."
        cd src/producers
        python3 producer.py
        ;;
    "dashboard"|"6")
        echo "📊 Starting Dashboard..."
        cd src/dashboard
        streamlit run dashboard.py
        ;;
    "all"|"7")
        check_dependencies
        start_docker
        echo "⏳ Waiting for services to initialize..."
        sleep 15
        
        echo "⚡ Starting Stream Processing..."
        cd src/stream_processing
        spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 stream_processing.py &
        STREAM_PID=$!
        
        echo "⏳ Waiting for stream processing to initialize..."
        sleep 10
        
        echo "🔄 Starting Consumers..."
        cd ../consumers
        python3 consumer_geolocation.py &
        python3 consumer_teammentions.py &
        python3 consumer_userverify.py &
        python3 consumer_verifieduserwindowed.py &
        
        echo "⏳ Waiting for consumers to initialize..."
        sleep 5
        
        echo "📊 Starting Dashboard..."
        cd ../dashboard
        streamlit run dashboard.py &
        DASH_PID=$!
        
        echo "📡 Starting Producer (this will run in foreground)..."
        cd ../producers
        python3 producer.py
        
        echo "🎉 Pipeline completed!"
        ;;
    "reset"|"8")
        echo "🧹 Resetting Kafka Topics..."
        bash scripts/reset-kafka.sh
        ;;
    "status"|"9")
        echo "📋 Checking Service Status..."
        check_service "Kafka" 9092
        check_service "PostgreSQL" 5432
        check_service "Streamlit Dashboard" 8501
        ;;
    "menu"|*)
        while true; do
            show_menu
            read -p "Enter your choice: " choice
            case $choice in
                1) bash "$0" setup ;;
                2) bash "$0" docker ;;
                3) bash "$0" stream ;;
                4) bash "$0" consumers ;;
                5) bash "$0" producer ;;
                6) bash "$0" dashboard ;;
                7) bash "$0" all ;;
                8) bash "$0" reset ;;
                9) bash "$0" status ;;
                0) echo "👋 Goodbye!"; exit 0 ;;
                *) echo "❌ Invalid option. Please try again." ;;
            esac
            echo ""
            read -p "Press Enter to continue..."
        done
        ;;
esac