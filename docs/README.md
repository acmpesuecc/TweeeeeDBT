# TweeeeeDBT

A comprehensive real-time streaming analytics pipeline for Twitter IPL data using Apache Kafka, Apache Spark, PostgreSQL, and Streamlit dashboard.

## 📁 Project Structure

```
TweeeeeDBT/
├── src/                          # Source code
│   ├── producers/                # Kafka producers
│   │   └── producer.py          # Main data producer
│   ├── consumers/                # Kafka consumers
│   │   ├── consumer_geolocation.py
│   │   ├── consumer_teammentions.py
│   │   ├── consumer_userverify.py
│   │   └── consumer_verifieduserwindowed.py
│   ├── stream_processing/        # Stream processing
│   │   └── stream_processing.py # Spark streaming logic
│   ├── batch_processing/         # Batch processing
│   │   └── batch_processing.py  # Batch analytics
│   └── dashboard/                # Web dashboard
│       ├── dashboard.py         # Streamlit dashboard
│       ├── dashboard_README.md  # Dashboard documentation
│       ├── generate_sample_data.py
│       └── .streamlit/          # Dashboard config
├── data/                         # Data files
│   └── IPL_2022_tweets.csv     # Source dataset
├── db/                          # Database files
│   ├── schema.sql              # Database schema
│   └── dbcheck.py              # Database utilities
├── docs/                        # Documentation
│   ├── CONTRIBUTING.md         # Contribution guidelines
│   ├── ProjectReport.pdf       # Project documentation
│   ├── image.png               # Architecture diagram
│   └── Requirement Specification/
├── scripts/                     # Utility scripts
│   └── reset-kafka.sh          # Kafka reset script
├── docker-compose.yaml          # Docker services
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🏗️ Architecture

![Architecture](docs/image.png)

## 📊 Dataset
[IPL 2022 Tweets Dataset](https://www.kaggle.com/datasets/kaushiksuresh147/ipl2020-tweets) - Download and place in `data/` directory.

## 🚀 Quick Start

### 1. Infrastructure Setup

**Kafka & Zookeeper:**
```bash
docker compose up -d
```

**Verify Kafka:**
```bash
docker ps # Check containers are running
docker exec -it tweeeeedbt-kafka-1 bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 2. Apache Spark Setup
**Requirements:** Java 17, Python 3.8.10+

```bash
# Download and install Spark
wget https://downloads.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz
tar -xvzf spark-3.5.5-bin-hadoop3.tgz
mv spark-3.5.5-bin-hadoop3 ~/spark

# Add to PATH
echo 'export SPARK_HOME=~/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 3. Database Setup

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

**Configure Database:**
```bash
# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS

# Create database and user
sudo -u postgres psql
CREATE DATABASE tweedbt;
CREATE USER <username> WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE tweedbt TO <username>;
\q

# Apply schema
psql -U <username> -d tweedbt -f db/schema.sql
```

### 4. Environment Configuration

Create `.env` file:
```env
POSTGRES_DB=tweedbt
POSTGRES_USER=<your_username>
POSTGRES_PASSWORD=<your_password>
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## 🏃‍♂️ Running the Pipeline 

**Reset Kafka (if needed):**
```bash
bash scripts/reset-kafka.sh
```

**Start Pipeline (in separate terminals, in order):**

1. **Stream Processing:**
```bash
cd src/stream_processing
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 stream_processing.py
```

2. **Start Consumers:**
```bash
cd src/consumers
python3 consumer_geolocation.py     # Terminal 1
python3 consumer_teammentions.py    # Terminal 2  
python3 consumer_userverify.py      # Terminal 3
python3 consumer_verifieduserwindowed.py # Terminal 4
```

3. **Start Producer:**
```bash
cd src/producers  
python3 producer.py
```

4. **Launch Dashboard:**
```bash
cd src/dashboard
streamlit run dashboard.py
```

## 📊 Analytics Dashboard

Access the real-time dashboard at: **http://localhost:8501**

### Features:
- **📈 Real-time Metrics**: Live tweet counts and system health
- **🗺️ Geographic Analytics**: Delhi vs Mumbai tweet distribution  
- **🏏 Team Analysis**: RCB vs CSK mention tracking
- **⚡ Performance Monitoring**: Batch vs streaming comparison
- **📊 Interactive Charts**: Plotly visualizations with filters
- **🔄 Auto-refresh**: Updates every 30 seconds

### Dashboard Pages:
1. **Overview** - Key metrics and system status
2. **Streaming Analytics** - Real-time tweet processing insights
3. **Batch vs Stream** - Performance comparison analysis
4. **Real-time Metrics** - Live monitoring dashboard

## 🛠️ Development

### Running Individual Components:

**Database Check:**
```bash
cd db
python3 dbcheck.py
```

**Batch Processing:**
```bash
cd src/batch_processing
python3 batch_processing.py
```

**Generate Sample Data:**
```bash
cd src/dashboard
python3 generate_sample_data.py
```

### Project Status:
- [x] ✅ Data Visualization Layer
- [x] ✅ Folder Structuring  
- [x] ✅ System Architecture Diagram
- [x] ✅ Streaming Pipeline Implementation
- [x] ✅ Interactive Dashboard
- [ ] 🔄 Dockerize Complete Pipeline

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- **Project Report**: [docs/ProjectReport.pdf](docs/ProjectReport.pdf)
- **Requirements**: [docs/Requirement Specification/](docs/Requirement%20Specification/)
- **Dashboard Guide**: [src/dashboard/dashboard_README.md](src/dashboard/dashboard_README.md)