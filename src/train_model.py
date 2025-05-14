import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
DATA_PATH  = BASE_DIR / "dataset" / "raw" / "ODI Cricket Data new.csv"
MODEL_DIR  = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ── Load & Clean ────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

# Remove extra dots from strike_rate (if any) then convert to numeric
df["strike_rate"] = (
    df["strike_rate"]
      .astype(str)
      .apply(lambda x: x.replace(".", "", x.count(".") - 1))
      .pipe(pd.to_numeric, errors="coerce")
)

# Encode categorical 'role' column
le = LabelEncoder()
df["role"] = le.fit_transform(df["role"].astype(str))

# ── Features & Target ────────────────────────────────────────────────────────────
features = ["strike_rate", "total_balls_faced", "total_matches_played", "matches_won", "matches_lost"]
X = df[features].copy().fillna(df[features].mean())
y = df["total_runs"]

# ── Train/Test Split ────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Model Training ──────────────────────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

# ── Evaluation ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

# ── Save Model ─────────────────────────────────────────────────────────────────
model_path = MODEL_DIR / "cricket_model.pkl"
joblib.dump(model, model_path)
print(f"✅ Model saved to: {model_path}")
