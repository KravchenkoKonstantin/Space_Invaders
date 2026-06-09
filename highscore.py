import json
import os

HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    data = load_leaderboard()
    if data:
        return data[0]
    return 0

def load_leaderboard():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            scores = data.get('scores', [])
            if not isinstance(scores, list):
                return []
            scores.sort(reverse=True)
            return scores[:5]
    except (json.JSONDecodeError, ValueError):
        return []

def save_highscore(score):
    scores = load_leaderboard()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:5]
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump({'scores': scores}, f)
    except IOError:
        pass 
    return len(scores) > 0 and score == scores[0]