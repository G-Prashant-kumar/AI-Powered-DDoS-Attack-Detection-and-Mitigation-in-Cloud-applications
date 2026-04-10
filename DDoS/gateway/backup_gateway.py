# # from flask import Flask, request, Response
# # import requests
# # import time
# # import csv

# # import joblib
# # from collections import defaultdict, deque
# # from flask import make_response

# # app = Flask(__name__)
# # TARGET_URL = "http://localhost:5001"

# # LOG_FILE = "traffic_log.csv"

# # def log_request(ip, method, path, size, status):
# #     with open(LOG_FILE, "a", newline="") as f:
# #         writer = csv.writer(f)
# #         writer.writerow([time.time(), ip, method, path, size, status])

# # model = joblib.load(r"d:/Learning/Final Year Project/DDoS/ddos_model.pkl")

# # WINDOW = 5
# # ip_logs = defaultdict(deque)


# # @app.route("/", defaults={"path": ""}, methods=["GET","POST"])
# # @app.route("/<path:path>", methods=["GET","POST"])
# # def proxy(path):
    

# #     now = time.time()
# #     ip = request.remote_addr

# #     # ---- LIVE FEATURE TRACKING ----
# #     ip_logs[ip].append(now)
# #     while ip_logs[ip] and now - ip_logs[ip][0] > WINDOW:
# #         ip_logs[ip].popleft()

# #     req_count = len(ip_logs[ip])
# #     avg_gap = (ip_logs[ip][-1] - ip_logs[ip][0]) / req_count if req_count > 1 else 0
# #     unique_urls = 1  # simple for demo

# #     prediction = model.predict([[req_count, avg_gap, unique_urls]])

# #     if prediction[0] == 1:
# #         return Response("Blocked: DDoS detected", status=429)

# #     # ---- ONLY IF NOT ATTACK ----
# #     method = request.method
# #     url = f"{TARGET_URL}/{path}" if path else f"{TARGET_URL}/"
# #     size = request.content_length or 0

# #     try:
# #         resp = requests.request(
# #             method,
# #             url,
# #             data=request.get_data(),
# #             headers={
# #                 key: value for key, value in request.headers
# #                 if key.lower() != "host"
# #             },
# #             timeout=5
# #         )
# #     except requests.exceptions.ConnectionError:
# #         return Response("Gateway Error: Backend unavailable", status=502)

# #     log_request(ip, method, path, size, resp.status_code)
# #     return Response(resp.content, resp.status_code, resp.headers.items())


# # if __name__ == "__main__":
# #     with open(LOG_FILE, "w", newline="") as f:
# #         csv.writer(f).writerow(
# #             ["timestamp", "ip", "method", "path", "size", "status"]
# #         )
# #     app.run(host="0.0.0.0", port=5000)


# from flask import Flask, request, Response
# import requests
# import time
# import csv

# import joblib
# from collections import defaultdict, deque

# app = Flask(__name__)

# # Backend app (protected service)
# TARGET_URL = "http://localhost:5001"

# # Log file
# LOG_FILE = "traffic_log.csv"

# # Load trained ML model
# model = joblib.load(r"d:/Learning/Final Year Project/DDoS/ddos_model.pkl")

# # Sliding window (seconds)
# WINDOW = 5
# ip_logs = defaultdict(deque)


# def log_request(ip, method, path, size, status):
#     with open(LOG_FILE, "a", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow([time.time(), ip, method, path, size, status])


# @app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
# @app.route("/<path:path>", methods=["GET", "POST"])
# def proxy(path):

#     # =====================================================
#     # 1️⃣ STATIC FILE HANDLING (CSS / JS / Images)
#     # =====================================================
#     # ---- BYPASS ML FOR STATIC FILES ----
#     if path.startswith("static/"):
#         url = f"{TARGET_URL}/{path}"
#         resp = requests.get(url, stream=True)

#         excluded_headers = {
#             "content-encoding",
#             "content-length",
#             "transfer-encoding",
#             "connection",
#         }

#         headers = [
#             (name, value)
#             for name, value in resp.headers.items()
#             if name.lower() not in excluded_headers
#         ]

#         response = Response(resp.content, resp.status_code)
#         for h in headers:
#             response.headers.add(*h)

#         return response


#     # =====================================================
#     # 2️⃣ ML-BASED DDoS DETECTION (PER IP)
#     # =====================================================
#     now = time.time()
#     ip = request.remote_addr

#     ip_logs[ip].append(now)

#     while ip_logs[ip] and now - ip_logs[ip][0] > WINDOW:
#         ip_logs[ip].popleft()

#     req_count = len(ip_logs[ip])
#     avg_gap = (
#         (ip_logs[ip][-1] - ip_logs[ip][0]) / req_count
#         if req_count > 1
#         else 0
#     )

#     unique_urls = 1  # simplified for live demo

#     prediction = model.predict([[req_count, avg_gap, unique_urls]])

#     if prediction[0] == 1 and not path.startswith("static/"):
#         return Response("Blocked: DDoS detected", status=429)


#     # =====================================================
#     # 3️⃣ FORWARD NORMAL TRAFFIC TO BACKEND
#     # =====================================================
#     method = request.method
#     url = f"{TARGET_URL}/{path}" if path else f"{TARGET_URL}/"
#     size = request.content_length or 0

#     try:
#         resp = requests.request(
#             method,
#             url,
#             data=request.get_data(),
#             headers={
#                 key: value
#                 for key, value in request.headers
#                 if key.lower() != "host"
#             },
#             timeout=5
#         )
#     except requests.exceptions.ConnectionError:
#         return Response("Gateway Error: Backend unavailable", status=502)

#     log_request(ip, method, path, size, resp.status_code)

#     response = Response(resp.content, resp.status_code)
#     for h in resp.headers.items():
#         response.headers.add(*h)

#     return response


# # =====================================================
# # START GATEWAY
# # =====================================================
# if __name__ == "__main__":
#     with open(LOG_FILE, "w", newline="") as f:
#         csv.writer(f).writerow(
#             ["timestamp", "ip", "method", "path", "size", "status"]
#         )

#     app.run(host="0.0.0.0", port=5000)

