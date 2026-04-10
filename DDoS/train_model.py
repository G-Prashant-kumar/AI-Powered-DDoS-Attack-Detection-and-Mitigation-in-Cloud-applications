import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv(r"d:/Learning/Final Year Project/DDoS/labeled_features.csv")
print("Loaded columns:", df.columns)

X = df[["req_count", "avg_gap", "unique_urls"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "ddos_model.pkl")
print("Model saved")
