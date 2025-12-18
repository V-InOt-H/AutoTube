import os
import asyncio
import edge_tts

DATA_DIR = "data"

# You can change this to any available Microsoft voice later
VOICE = "en-US-GuyNeural"   # male-ish English voice
RATE = "+0%"                # speed, e.g. "-10%", "+20%"

async def generate_voice():
    script_path = os.path.join(DATA_DIR, "script.txt")
    if not os.path.exists(script_path):
        raise FileNotFoundError("data/script.txt not found. Run script_caption_hashtags.py first.")

    with open(script_path, "r") as f:
        text = f.read().strip()

    if not text:
        raise ValueError("Script is empty.")

    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, "voice.mp3")

    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE)
    await communicate.save(out_path)
    print(f"✅ Microsoft voice generated: {out_path}")

def main():
    asyncio.run(generate_voice())

if __name__ == "__main__":
    main()
