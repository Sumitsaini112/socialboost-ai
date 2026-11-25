
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI, OpenAIError

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="SocialBoost AI")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def home():
    index_file = BASE_DIR / "static" / "index.html"
    return index_file.read_text(encoding="utf-8")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": "SocialBoost AI",
        "ai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


def get_ai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI is not configured yet. Please try again later."
        )

    return OpenAI(api_key=api_key)


def clean_input(payload, field, default=""):
    value = payload.get(field, default)

    if not isinstance(value, str):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field}."
        )

    value = value.strip()

    if len(value) > 120:
        raise HTTPException(
            status_code=400,
            detail=f"{field} must be 120 characters or fewer."
        )

    return value


def validate_options(payload):
    platform = clean_input(payload, "platform", "YouTube")
    language = clean_input(payload, "language", "English")

    allowed_platforms = ["YouTube", "Instagram", "Facebook"]
    allowed_languages = ["English", "Hindi", "Hinglish"]

    if platform not in allowed_platforms:
        raise HTTPException(
            status_code=400,
            detail="Invalid platform."
        )

    if language not in allowed_languages:
        raise HTTPException(
            status_code=400,
            detail="Invalid language."
        )

    return platform, language



def ask_ai(prompt):
    client = get_ai_client()

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
            max_output_tokens=650
        )

        result = response.output_text.strip()

        if not result:
            raise HTTPException(
                status_code=502,
                detail="AI returned an empty response. Try again."
            )

        return result

    except OpenAIError as e:
        print(
            f"OPENAI API ERROR: {type(e).__name__}: {e}",
            flush=True
        )
        raise HTTPException(
            status_code=502,
            detail="AI service error. Check Render logs."
        )
        


@app.post("/api/ideas")
def ideas(payload: dict):
    topic = clean_input(payload, "topic")

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic or niche first."
        )

    platform, language = validate_options(payload)

    prompt = f"""
You are a helpful social media content strategist.

Create exactly 5 original, specific content ideas.

Topic or niche: {topic}
Platform: {platform}
Language: {language}

Requirements:
- Make ideas engaging and useful for the selected platform.
- Avoid generic filler and repeated ideas.
- Do not invent facts or promise viral results.
- Keep each idea concise.
- Write one idea per line.
- Do not add an introduction or conclusion.
"""

    result = ask_ai(prompt)

    ideas_list = []

    for line in result.splitlines():
        line = re.sub(
            r"^\s*(?:\d+[\.\)]|[-*])\s*",
            "",
            line
        ).strip()

        if line:
            ideas_list.append(line)

    return {
        "ideas": ideas_list[:5],
        "note": f"AI-generated ideas for {platform} in {language}. Review and personalize before publishing."
    }


@app.post("/api/caption")
def caption(payload: dict):
    topic = clean_input(payload, "topic")

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Please enter your post topic first."
        )

    platform, language = validate_options(payload)

    prompt = f"""
You are an expert social media caption writer.

Create a useful, engaging caption for this post.

Post topic: {topic}
Platform: {platform}
Language: {language}

Requirements:
- Make the caption specific to the topic.
- Use a natural and friendly tone.
- Include a suitable call to action.
- Add 5 to 10 relevant hashtags.
- Do not use unrelated or misleading hashtags.
- Do not invent facts.
- Do not promise views, followers or viral reach.

Use exactly this format:

CAPTION:
Write the caption here.

HASHTAGS:
Write the hashtags here.
"""

    result = ask_ai(prompt)

    if "HASHTAGS:" in result:
        parts = result.split("HASHTAGS:", 1)
        caption_text = parts[0].replace("CAPTION:", "").strip()
        hashtags = parts[1].strip()
    else:
        caption_text = result.replace("CAPTION:", "").strip()
        hashtags = ""

    return {
        "caption": caption_text,
        "hashtags": hashtags,
        "note": f"AI-generated draft for {platform}. Review facts and personalize before publishing."
    }

