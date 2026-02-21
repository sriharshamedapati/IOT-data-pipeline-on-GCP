# 🚀 Real-Time IoT Data Pipeline

**Pub/Sub Emulator → Consumer → MySQL (Dockerized)**

---

## 📌 Project Overview

This project implements a fully containerized, real-time IoT data pipeline using a producer-consumer architecture.

Simulated IoT sensor readings are streamed through a Google Cloud Pub/Sub emulator, validated in real-time by a consumer service, and persisted into a MySQL database.

The entire system runs locally using Docker Compose, ensuring reproducibility, portability, and ease of evaluation.

---

## 🧱 Architecture

```
Producer → Pub/Sub Emulator → Consumer → MySQL Database
```

### 🔄 Data Flow

1. The **Producer** generates simulated IoT sensor readings.
2. Messages are published to a **Pub/Sub topic**.
3. The **Consumer** subscribes to the topic.
4. Incoming messages undergo validation.
5. Valid records are inserted into MySQL.
6. Invalid messages are safely handled without disrupting the pipeline.

---

## 🛠 Technologies Used

* Python 3.10
* Google Cloud Pub/Sub Emulator
* MySQL 8.0
* Docker
* Docker Compose

---

## 📁 Repository Structure

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

## ⚙️ Setup Instructions

### ✅ Prerequisites

* Docker Desktop
* Git

---

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd <project-folder>
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the root directory using `.env.example`.

Example:

```env
GCP_PROJECT_ID=local-project
PUBSUB_TOPIC_RAW=iot-sensor-data-raw
PUBSUB_TOPIC_DLQ=iot-sensor-data-dlq
MYSQL_ROOT_PASSWORD=password123
MYSQL_DATABASE=iot_data
```

---

### 3️⃣ Build and Run the Pipeline

```bash
docker compose up --build
```

This starts:

* MySQL database
* Pub/Sub emulator
* Consumer service

---

## 🧪 Running the Producer

Open a new terminal:

```bash
cd producer
python app.py
```

This continuously publishes sensor readings to the Pub/Sub topic.

---

## 🧹 Data Quality Rules

The consumer enforces strict validation rules:

### Required Fields

* `device_id`
* `timestamp_utc`
* `temperature_celsius`
* `humidity_percent`

### Validation Checks

* Temperature range: **-50°C to 100°C**
* Humidity range: **0% to 100%**
* ISO 8601 timestamp validation
* JSON structure validation

Only valid messages are inserted into the database.

---

## 🛡 Error Handling Strategy

* Graceful try/except blocks around message processing
* Database connection retry logic on startup
* Invalid messages logged without crashing consumer
* Message acknowledgment prevents pipeline blockage

The system is fault-tolerant and resilient to malformed data.

---

## 🔍 Verifying Data in MySQL

Enter the MySQL container:

```bash
docker exec -it mysql-db mysql -u root -p
```

Enter password:

```
password123
```

Then run:

```sql
USE iot_data;
SELECT COUNT(*) FROM sensor_readings;
SELECT * FROM sensor_readings LIMIT 10;
```

You should see inserted sensor records.

---

## 📸 Demonstration

Include screenshots showing:

* Docker containers running
* Consumer logs processing messages
* MySQL query results displaying inserted records

---

## ✨ Key Features

* Real-time message streaming
* Event-driven architecture
* Data validation layer
* Fault-tolerant consumer
* Fully containerized local deployment
* Clean environment variable management

---

## 🔮 Future Enhancements

* Dead Letter Queue (DLQ) implementation
* Automated unit/integration tests
* Deployment to Google Cloud (Pub/Sub + Cloud SQL)
* Observability and monitoring dashboard
