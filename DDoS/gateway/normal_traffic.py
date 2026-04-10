import requests
import time
import random

URLS = [
    "http://13.234.122.135:5000/",
    "http://13.234.122.135:5000/login",
    "http://13.234.122.135:5000/profile",
    "http://13.234.122.135:5000/data",
    "http://13.234.122.135:5000/search"
]

while True:
    requests.get(random.choice(URLS))
    time.sleep(1)
