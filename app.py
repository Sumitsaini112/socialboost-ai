import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="SocialBoost AI")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SocialBoost AI"}

@app.post("/api/ideas")
def ideas(payload: dict):
    topic = str(payload.get("topic", "your niche")).strip()[:120]
    platform = str(payload.get("platform", "YouTube")).strip()[:40]
    return {
        "ideas": [
            f"3 mistakes beginners make in {topic}",
            f"The truth about {topic} nobody explains",
            f"Try this {topic} tip for 7 days",
            f"{topic}: myth vs fact",
            f"Before you post about {topic}, know this"
        ],
        "note": f"Draft ideas for {platform}. Adapt them to your own original content."
    }

@app.post("/api/caption")
def caption(payload: dict):
    topic = str(payload.get("topic", "your topic")).strip()[:120]
    platform = str(payload.get("platform", "Instagram")).strip()[:40]
    return {
        "caption": f"{topic} — here's one thing worth knowing. Save this post and share your experience in the comments.\\n\\nWhat would you like to learn next?",
        "hashtags": "#contentcreator #creatorjourney #socialmedia #learnwithme",
        "note": f"Starter draft for {platform}; review facts and personalize before publishing."
    }
