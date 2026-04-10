from flask import Flask, request, Response, send_from_directory, render_template
import requests
import time
import csv
import os

import joblib
from collections import defaultdict, deque

# -------------------------------------------------
# PATH SETUP
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
print("Gateway static dir:", STATIC_DIR)

# -------------------------------------------------
# APP SETUP
# -------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../app/templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)
TARGET_URL = "http://localhost:5001"

LOG_FILE = "traffic_log.csv"
model = joblib.load(r"d:/Learning/Final Year Project/DDoS/ddos_model.pkl")

WINDOW = 5
ip_logs = defaultdict(deque)

blocked_ips = {}
BLOCK_TIME = 30

total_requests = 0
blocked_requests = 0
requests_per_ip = {}

unique_blocked_ips = set()

url_rate_logs = defaultdict(lambda: defaultdict(deque))
RATE_LIMIT = 25        # max requests
RATE_WINDOW = 5        # seconds

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def log_request(ip, method, path, size, status):
    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(
            [time.time(), ip, method, path, size, status]
        )

# STATIC
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

# LOGS
@app.route("/logs")
def view_logs():
    with open(LOG_FILE, "r") as f:
        logs = f.read()

    return render_template("logs.html", logs=logs)

# STATS
@app.route("/stats")
def stats():
    active_attackers = len(blocked_ips)
    total_unique_attackers = len(unique_blocked_ips)

    return render_template(
        "stats.html",
        total_requests=total_requests,
        blocked_requests=blocked_requests,
        active_attackers=active_attackers,
        total_unique_attackers=total_unique_attackers,
        requests_per_ip=requests_per_ip,
        blocked_ips=unique_blocked_ips
    )

# PROXY
@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
        
def proxy(path):

    # Serve static files directly from backend
    if path.startswith("static/"):
        url = f"{TARGET_URL}/{path}"
        resp = requests.get(url, stream=True)

        excluded_headers = [
            'content-encoding',
            'content-length',
            'transfer-encoding',
            'connection',
            'content-security-policy'
        ]

        response = Response(resp.content, resp.status_code,
                            content_type=resp.headers.get('Content-Type'))

        for name, value in resp.headers.items():
            if name.lower() not in excluded_headers:
                response.headers.add(name, value)

        return response
  
    # ML-based DDoS detection    
    now = time.time()
    ip = request.remote_addr
    global total_requests, blocked_requests, requests_per_ip

    total_requests += 1

    if ip not in requests_per_ip:
        requests_per_ip[ip] = 0
    requests_per_ip[ip] += 1

    # ----------------------------
    # Check if IP already blocked
    # ----------------------------
    if ip in blocked_ips:
        if time.time() - blocked_ips[ip] < BLOCK_TIME:
            log_request(ip, request.method, path, 0, 429)
            return Response("IP temporarily blocked", status=429)
        else:
            del blocked_ips[ip]

    # ----------------------------
    # Rate limit per IP + URL
    # ----------------------------
    url_rate_logs[ip][path].append(now)

    while url_rate_logs[ip][path] and now - url_rate_logs[ip][path][0] > RATE_WINDOW:
        url_rate_logs[ip][path].popleft()

    if len(url_rate_logs[ip][path]) > RATE_LIMIT:
        blocked_ips[ip] = time.time()
        blocked_requests += 1
        unique_blocked_ips.add(ip)
        print(f"[RATE LIMIT] Blocking IP {ip} for flooding {path}")
        log_request(ip, request.method, path, 0, 429)
        return Response("Rate limit exceeded", status=429)

    # ----------------------------
    # ML-based traffic analysis
    # ----------------------------
    ip_logs[ip].append(now)
    while ip_logs[ip] and now - ip_logs[ip][0] > WINDOW:
        ip_logs[ip].popleft()

    req_count = len(ip_logs[ip])
    avg_gap = (
        (ip_logs[ip][-1] - ip_logs[ip][0]) / req_count
        if req_count > 1 else 0
    )
    unique_urls = 1

    prediction = model.predict([[req_count, avg_gap, unique_urls]])
    prob = model.predict_proba([[req_count, avg_gap, unique_urls]])

    print("Attack probability:", prob[0][1])
    print(f"IP={ip} | req_count={req_count} | avg_gap={avg_gap:.4f} | prediction={prediction[0]}")

    # ----------------------------
    # If attack detected → block IP
    # ----------------------------
    if prediction[0] == 1:
        blocked_requests += 1
        blocked_ips[ip] = time.time()
        unique_blocked_ips.add(ip)

        print(f"[ATTACK DETECTED] Blocking IP {ip} for 30 sec")
        log_request(ip, request.method, path, 0, 429)
        return Response("Blocked: DDoS detected", status=429)

    # ----------------------------
    # Forward clean traffic
    # ----------------------------
    method = request.method
    url = f"{TARGET_URL}/{path}" if path else f"{TARGET_URL}/"
    size = request.content_length or 0

    try:
        resp = requests.request(
            method,
            url,
            data=request.get_data(),
            headers={
                k: v for k, v in request.headers.items()
                if k.lower() != "host"
            },
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        return Response("Gateway Error: Backend unavailable", status=502)

    log_request(ip, method, path, size, resp.status_code)

    excluded_headers = [
        'content-encoding',
        'content-length',
        'transfer-encoding',
        'connection',
        'content-security-policy'
    ]

    response = Response(
        resp.content,
        resp.status_code,
        content_type=resp.headers.get('Content-Type')
    )

    for name, value in resp.headers.items():
        if name.lower() not in excluded_headers:
            response.headers.add(name, value)

    return response

# -------------------------------------------------
# START
# -------------------------------------------------
if __name__ == "__main__":
    with open(LOG_FILE, "w", newline="") as f:
        csv.writer(f).writerow(
            ["timestamp", "ip", "method", "path", "size", "status"]
        )

    app.run(host="0.0.0.0", port=5000)

    
