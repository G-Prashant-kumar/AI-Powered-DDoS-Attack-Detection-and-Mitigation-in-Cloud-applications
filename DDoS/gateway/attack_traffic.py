import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://13.201.43.221:5000/login"

def send():
    requests.get(URL)

with ThreadPoolExecutor(max_workers=50) as executor:
    for _ in range(500):
        executor.submit(send)
