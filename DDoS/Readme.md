# 🚀 AI-Powered DDoS Detection and Mitigation for Cloud Applications

## 📌 Overview

This project presents a **real-time AI-powered gateway system** designed to detect and mitigate **application-layer DDoS attacks** in cloud-hosted web applications.

The system acts as an **intelligent reverse proxy**, analyzing incoming traffic using machine learning and blocking malicious requests before they reach the backend server.

---

## 🎯 Objectives

* Detect abnormal traffic patterns using ML
* Prevent DDoS attacks in real-time
* Maintain availability of cloud applications
* Provide traffic monitoring and logging
* Simulate real-world cloud security architecture

---

## 🧠 Key Features

### 🔹 Multi-Layer Security Architecture

* IP-based blocking
* Rate limiting (IP + URL)
* ML-based anomaly detection
* Temporary attacker isolation

### 🔹 Real-Time Traffic Analysis

* Tracks request frequency
* Calculates request gaps
* Monitors endpoint access behavior

### 🔹 Machine Learning Detection

* Uses behavioral features:

  * `req_count`
  * `avg_gap`
  * `unique_urls`
* Classifies traffic as:

  * Normal (0)
  * Attack (1)

### 🔹 Automated Mitigation

* Blocks attacker IPs
* Returns HTTP 429 (Too Many Requests)
* Temporary blocking mechanism

### 🔹 Logging & Monitoring

* Logs all traffic into CSV
* Tracks:

  * Total requests
  * Blocked requests
  * Accepted requests
  * Requests per IP
  * Unique attackers

---

## 🏗️ System Architecture

```
User Request
     ↓
Cloud Gateway (Flask Reverse Proxy)
     ↓
[Layer 1] IP Block Check
     ↓
[Layer 2] Rate Limiting (IP + URL)
     ↓
[Layer 3] Feature Extraction
     ↓
[Layer 4] ML Model Prediction
     ↓
[Layer 5] Mitigation (Block / Allow)
     ↓
Backend Web Application
     ↓
Logs + Dataset
```

---

## ⚙️ Technologies Used

| Category        | Technology    |
| --------------- | ------------- |
| Backend         | Flask         |
| ML Model        | Random Forest |
| Data Processing | Pandas, NumPy |
| Model Saving    | Joblib        |
| HTTP Proxy      | Requests      |
| Deployment      | AWS / Render  |
| Logging         | CSV           |

---

## 🧪 Machine Learning Model

### Model Used:

* **Random Forest Classifier**

### Features:

* Request Count (req_count)
* Average Time Gap (avg_gap)
* Unique URLs Accessed (unique_urls)

### Training Process:

1. Collect traffic logs
2. Convert to feature dataset
3. Label normal vs attack traffic
4. Train model
5. Save using `joblib`

---

## 📁 Project Structure

```
DDoS_Project/
│
├── gateway/
│   ├── gateway.py
│   ├── ddos_model.pkl
│   ├── requirements.txt
│
├── app/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── requirements.txt
│
├── train_model.py
├── labeled_features.csv
├── traffic_log.csv
├── README.md
```

---

## 🔄 Workflow

1. User sends request
2. Gateway intercepts traffic
3. Checks:

   * Blocked IP
   * Rate limit
4. Extracts features
5. ML model predicts behavior
6. If attack:

   * Block request
   * Add IP to block list
7. Else:

   * Forward request to backend

---

## 📊 Metrics Tracked

* Total Requests
* Accepted Requests
* Blocked Requests
* Active Blocked IPs
* Unique Attackers
* Requests per IP

---

## ☁️ Cloud Deployment

### 🔹 AWS Deployment (Recommended)

**Architecture:**

```
Internet
   ↓
AWS EC2 (Gateway)
   ↓
AWS EC2 / App Server (Backend)
```

**Steps:**

1. Launch EC2 instance
2. Install Python & dependencies
3. Upload project files
4. Run:

   ```bash
   python app.py
   python gateway.py
   ```
5. Expose ports using Security Groups

---

## 🔐 Security Layers Implemented

| Layer             | Description                  |
| ----------------- | ---------------------------- |
| IP Blocking       | Blocks known attackers       |
| Rate Limiting     | Prevents request flooding    |
| ML Detection      | Identifies abnormal behavior |
| Mitigation Engine | Blocks malicious traffic     |
| Logging           | Stores traffic data          |
| Monitoring        | Displays system stats        |

---

## 🚀 How to Run Locally

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Backend

```bash
python app.py
```

### Step 3: Run Gateway

```bash
python gateway.py
```

### Step 4: Access

```
http://localhost:5000
```

---

## ⚠️ Limitations

* Single-IP simulation (not fully distributed)
* Basic feature set
* Manual model retraining
* No deep packet inspection

---

## 🔮 Future Enhancements

* Multi-IP distributed attack simulation
* Deep learning models
* Real-time auto-retraining
* Integration with AWS WAF / Cloudflare
* Dashboard with charts (Grafana)

---

## 💡 Conclusion

This project demonstrates a **practical implementation of AI-driven DDoS detection and mitigation** using a multi-layer security approach. It closely resembles real-world cloud security systems and provides a scalable foundation for advanced threat protection.

---

## 👨‍💻 Author

Final Year Project – AI-Based Cloud Security System
