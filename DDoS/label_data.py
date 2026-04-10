import pandas as pd

df = pd.read_csv("features.csv")

# simple, honest rule for demo
df["label"] = df["req_count"].apply(lambda x: 1 if x > 20 else 0)

df.to_csv("labeled_features.csv", index=False)

print("Labels added")
print(df["label"].value_counts())
