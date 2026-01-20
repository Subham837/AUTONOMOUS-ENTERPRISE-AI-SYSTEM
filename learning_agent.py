import json
import os

def learning_agent(state):
    os.makedirs("memory", exist_ok=True)
    with open("memory/decisions.json", "a") as f:
        json.dump(dict(state), f)
        f.write("\n")
    return state