import os
import json
import requests
import re
import sys

MODEL = "llama3.2:1b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DATA_DIR = "data"

PROMPT = """
You MUST return ONLY a valid JSON object with EXACTLY these five keys:
"title", "description", "hashtags", "script", "image_query".

Format STRICTLY like this:

{
  "title": "...",
  "description": "...",
  "hashtags": "...",
  "script": "...",
  "image_query": "..."
}

Do NOT add explanations.
Do NOT add extra words.
Do NOT add markdown.
Return ONLY the JSON object.

=====================
CONTENT RULES:
=====================

TOPIC:
- Must be a car fact, car engineering detail, automotive history, supercar feature, or racing fact.

TITLE RULES:
- Max 55 characters.
- Must include exactly ONE emoji.
- No quotes.
- No hashtags.

DESCRIPTION RULES:
- 1–2 short sentences only.
- No emojis.
- No hashtags.

HASHTAG RULES:
- 5 to 12 hashtags.
- Space-separated, no commas.

IMAGE_QUERY RULES:
- 3–6 words.
- MUST be about cars or engines.
- Must based on our script and title 
- No emojis, no hashtags, no quotes.

=====================
30-SECOND SCRIPT RULES:
=====================

LENGTH:
- Script MUST be 6 to 8 sentences.
- Script MUST be 70 to 95 words.
- Script MUST sound natural when spoken aloud.
- Style should feel like storytelling.

STYLE:
- Conversational, energetic, simple English.
- No emojis.
- No hashtags.
- No references to YouTube or "video".
- No filler lines like "hi guys" or "subscribe".
- No repeated sentences.

STRUCTURE:
1. Hook sentence that grabs attention fast.
2. Introduce the car or technology.
3. Explain the problem or challenge.
4. Reveal the surprising fact.
5. Explain the impact.
6. Add a rare/unknown twist.
7. Why it matters.
8. Strong closing sentence with a punch.

Return ONLY the JSON.
""".strip()


def call_ollama(prompt: str) -> str:
    """Call Ollama and return the raw response text."""
    print("➡️  Calling Ollama at", OLLAMA_URL)
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 220,   # allow longer outputs
            "temperature": 0.8,
        },
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=150)
    except requests.exceptions.RequestException as e:
        print("❌ Could not connect to Ollama.")
        print("   Is `ollama serve` running and is llama3.2:1b pulled?")
        print("Error details:", e)
        sys.exit(1)

    if resp.status_code != 200:
        print("❌ Ollama returned HTTP", resp.status_code)
        print("Body:", resp.text[:400])
        sys.exit(1)

    data = resp.json()
    return data.get("response", "")

import json
import re

def extract_json(text):
    """
    Extract and repair JSON from messy LLM output.
    Always returns a dict. Never returns None.
    """

    # 1️⃣ Try to detect the first {...} block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        block = match.group(0)
        try:
            return json.loads(block)
        except:
            pass  # Try repair below

    # 2️⃣ Try JSON repair — extract pairs manually
    pairs = re.findall(r'"([^"]+)":\s*"([^"]*)"', text)
    if pairs:
        result = {k: v for k, v in pairs}
        return result  # Always valid dict

    # 3️⃣ If absolutely nothing found: return placeholder instead of None
    return {
        "title": "Unknown Title",
        "description": "No description generated.",
        "hashtags": "#cars",
        "script": "No script generated.",
        "image_query": "car engine"
    }

def count_sentences(text: str) -> int:
    parts = re.split(r"[.!?]+", text)
    return len([p for p in parts if p.strip()])


def count_words(text: str) -> int:
    return len(re.findall(r"\w+", text))

def main():
    print("🚀 script_caption_hashtags_ollama.py STARTED")
    print("🤖 Asking Ollama (1B) for car content...")

    raw = call_ollama(PROMPT)

    print("\n📝 Raw AI Output:")
    print(raw)

    try:
        data = extract_json(raw)
    except Exception as e:
        print("❌ JSON extraction error")
        print("Raw output from model:\n", raw)
        raise e

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    hashtags = data.get("hashtags", "").strip()
    script = data.get("script", "").strip()
    image_query = data.get("image_query", "").strip()

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(os.path.join(DATA_DIR, "title.txt"), "w") as f:
        f.write(title)
    with open(os.path.join(DATA_DIR, "description.txt"), "w") as f:
        f.write(description)
    with open(os.path.join(DATA_DIR, "hashtags.txt"), "w") as f:
        f.write(hashtags)
    with open(os.path.join(DATA_DIR, "script.txt"), "w") as f:
        f.write(script)
    with open(os.path.join(DATA_DIR, "image_query.txt"), "w") as f:
        f.write(image_query)

    print("\n✅ AI Content Generated Successfully!")
    print("Title:", title)
    print("Image query:", image_query)

if __name__ == "__main__":
    main()
