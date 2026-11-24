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
        line = re.sub(r"^\s*(?:\d+[\.\)]|[-*])\s*", "", line).strip()
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
    
