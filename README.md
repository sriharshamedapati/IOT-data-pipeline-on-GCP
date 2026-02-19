# 🚀 Real-Time IoT Data Pipeline (Pub/Sub → Consumer → MySQL)

## 📌 Project Overview

This project implements a real-time IoT data pipeline using a producer-consumer architecture.

The system simulates IoT sensor data generation, streams the data through a Pub/Sub messaging system, processes and validates the data in real time, and stores validated records in a MySQL database.

The entire pipeline runs locally using Docker Compose for reproducibility and easy deployment.

---

## 🧱 Architecture

```

Producer → Pub/Sub Emulator → Consumer → MySQL Database

```

### Data Flow

1. Producer generates simulated sensor readings.
2. Messages are published to Google Pub/Sub emulator.
3. Consumer subscribes to messages.
4. Data validation rules are applied.
5. Valid data is inserted into MySQL.

---

## ⚙️ Technologies Used

- Python
- Google Cloud Pub/Sub Emulator
- MySQL
- Docker
- Docker Compose

---

## 📁 Project Structure

```

project-root/
│
├── producer/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── consumer/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── docker-compose.yml
├── db_init.sql
├── .env.example
└── README.md

```

---

## 🔧 Setup Instructions

### Prerequisites

- Docker Desktop installed
- Git installed

---

### Clone Repository

```

git clone <your-repo-link>
cd <project-folder>

```

---

### Configure Environment Variables

Create `.env` file based on `.env.example`.

Example:

```

GCP_PROJECT_ID=local-project
PUBSUB_TOPIC_RAW=iot-sensor-data-raw
PUBSUB_TOPIC_DLQ=iot-sensor-data-dlq
MYSQL_ROOT_PASSWORD=password123
MYSQL_DATABASE=iot_data

```

---

### Run the Pipeline

```

docker compose up --build

```

This will start:

- MySQL container
- Pub/Sub emulator
- Consumer service

---

## 🧪 Running Producer (Data Generation)

Open a new terminal:

```

cd producer
python app.py

```

This will continuously publish sensor data messages.

---

## ✅ Data Quality Rules

The consumer validates incoming data:

- Required fields:
  - device_id
  - timestamp_utc
  - temperature_celsius
  - humidity_percent

- Temperature range check (-50 to 100°C)
- Humidity range check (0 to 100%)
- ISO timestamp validation

Invalid data is handled safely without breaking the pipeline.

---

## 🛡 Error Handling Strategy

- Try/except blocks around processing logic
- Invalid messages logged
- Message acknowledgment ensures no processing blockage
- Database connection retry logic prevents startup failures

---

## 🔍 Verifying Data in MySQL

Run:

```

docker exec -it mysql-db mysql -u root -p

```

Enter password:

```

password123

```

Then:

```

USE iot_data;
SELECT * FROM sensor_readings;

```

You should see inserted sensor records.

---

## 📸 Demo / Screenshots

(Add screenshots here)

- Docker containers running
- Consumer logs showing message processing
- MySQL query results

---

## 📊 Pipeline Features

- Real-time streaming simulation
- Message-driven architecture
- Data validation layer
- Fault-tolerant consumer
- Containerized deployment

---

## ⭐ Future Improvements

- Dead Letter Queue implementation
- Automated testing
- Cloud deployment
- Monitoring dashboard
