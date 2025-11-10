# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import math

app = FastAPI(title="Emotion Analysis API")

# ---- Input Schema ----
class TextInput(BaseModel):
    text: str

# ---- Example simple emotion logic ----
# You can replace this with your actual model or library logic
def analyze_emotions(text: str) -> Dict[str, float]:
    text = text.lower()
    emotions = {
        "joy": text.count("joy") + text.count("happy"),
        "sadness": text.count("sad") + text.count("grief"),
        "fear": text.count("fear") + text.count("anxiety"),
        "anger": text.count("anger") + text.count("hate"),
        "wonder": text.count("wonder") + text.count("mystery"),
    }

    # Normalize to weights (so they sum to 1)
    total = sum(emotions.values())
    if total > 0:
        for k in emotions:
            emotions[k] = round(emotions[k] / total, 2)
    else:
        # Neutral fallback
        emotions = {"neutral": 1.0}
    return emotions

# ---- API Endpoint ----
@app.post("/analyze")
def analyze_text(input: TextInput):
    emotions = analyze_emotions(input.text)
    return {"emotions": emotions}
