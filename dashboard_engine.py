import json
import matplotlib.pyplot as plt
from collections import Counter
import os


def plot_history(history_file="memory/optimization_history.json"):

    # Create dashboard folder automatically
    os.makedirs("dashboard", exist_ok=True)

    # Load history
    with open(history_file, "r") as f:
        history = json.load(f)

    repairs = []
    scores = []
    confidence = []
    slack = []

    for item in history:
        repairs.append(item["repair"])
        scores.append(item["score"])
        confidence.append(item["confidence"])
        slack.append(item["slack"])

    # -------------------------
    # Score Trend
    # -------------------------
    plt.figure("Optimization Score Trend", figsize=(10,5))

    plt.plot(scores, marker='o')
    plt.title("Optimization Score Trend")
    plt.xlabel("Run")
    plt.ylabel("Score")
    plt.grid(True)

    plt.savefig("dashboard/score_trend.png")

    plt.show(block=True)
    plt.clf()
    plt.close('all')

    # -------------------------
    # Confidence Trend
    # -------------------------
    plt.figure("Decision Confidence Trend", figsize=(10,5))

    plt.plot(confidence, marker='o')
    plt.title("Decision Confidence Trend")
    plt.xlabel("Run")
    plt.ylabel("Confidence (%)")
    plt.grid(True)

    plt.savefig("dashboard/confidence_trend.png")

    plt.show(block=True)
    plt.clf()
    plt.close('all')

    # -------------------------
    # Slack Trend
    # -------------------------
    plt.figure("Worst Slack History", figsize=(10,5))

    plt.plot(slack, marker='o')
    plt.title("Worst Slack History")
    plt.xlabel("Run")
    plt.ylabel("Slack")
    plt.grid(True)

    plt.savefig("dashboard/slack_history.png")

    plt.show(block=True)
    plt.clf()
    plt.close('all')

    # -------------------------
    # Repair Frequency
    # -------------------------
    repair_count = Counter(repairs)

    plt.figure("Repair Selection Frequency", figsize=(8,5))

    plt.bar(repair_count.keys(), repair_count.values())
    plt.title("Repair Selection Frequency")
    plt.xlabel("Repair")
    plt.ylabel("Count")

    plt.savefig("dashboard/repair_frequency.png")

    plt.show(block=True)
    plt.clf()
    plt.close('all')