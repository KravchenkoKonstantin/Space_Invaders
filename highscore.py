import json
import os

HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('highscore', 0)
    return 0

def save_highscore(score):
    current = load_highscore()
    if score > current:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump({'highscore': score}, f)
        return True
    return False
import os

HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('highscore', 0)
    return 0

def save_highscore(score):
    current = load_highscore()
    if score > current:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump({'highscore': score}, f)
        return True
    return False