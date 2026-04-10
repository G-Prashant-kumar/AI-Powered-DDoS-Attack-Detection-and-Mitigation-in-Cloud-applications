import pandas as pd

df = pd.read_csv("traffic_log.csv")

WINDOW = 5  # seconds

df["window"] = (df["timestamp"] // WINDOW) * WINDOW

features = df.groupby(["ip", "window"]).agg(
    req_count=("timestamp", "count"),
    avg_gap=("timestamp", lambda x: x.diff().mean()),
    unique_urls=("path", "nunique")
).reset_index()

features = features.fillna(0)
features.to_csv("features.csv", index=False)

print(features.head())
