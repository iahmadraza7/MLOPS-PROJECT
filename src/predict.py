# predict.py

import joblib
import pandas as pd
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "cricket_model.pkl"

# ── Load Model ───────────────────────────────────────────────────────────────────
model = joblib.load(MODEL_PATH)

# ── Example Prediction ───────────────────────────────────────────────────────────
new_player = pd.DataFrame(
    [[85.0, 12000, 500, 300, 200]],
    columns=["strike_rate", "total_balls_faced", "total_matches_played", "matches_won", "matches_lost"]
)
predicted_runs = model.predict(new_player)
print(f"Predicted Total Runs: {predicted_runs[0]:.2f}")
