import json
import os
from datetime import datetime

HISTORY_FILE = "memory/optimization_history.json"


def save_history(candidate, score, slack, confidence):

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "repair": candidate,
        "score": score,
        "slack": slack,
        "confidence": confidence
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)