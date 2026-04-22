import json
import os

MEMORY_FILE = "memory/repair_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def update_memory(pattern, repair_choice):

    memory = load_memory()

    if pattern not in memory:
        memory[pattern] = {}

    if repair_choice not in memory[pattern]:
        memory[pattern][repair_choice] = 0

    memory[pattern][repair_choice] += 1

    save_memory(memory)

def predict_best_repair(pattern):

    memory = load_memory()

    if pattern not in memory:
        return None

    repairs = memory[pattern]

    best = max(repairs, key=repairs.get)

    return best