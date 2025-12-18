import subprocess
import sys
import shutil
import os

def clean_assets():
    folders = [
        "assets/audio",
        "assets/videos",
        "assets/subtitles",
        "assets/images"
    ]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

clean_assets()

steps = [
    ("Generating AI content", "script_caption_hashtags_ollama.py"),
    ("Reviewing content", "review_and_confirm.py"),
    ("Creating Microsoft voiceover", "voiceover_ms.py"),
    ("Downloading images", "image_downloader.py"),
    ("Making slideshow video", "video_creator_advanced.py"),
    ("Uploading to YouTube", "youtube_uploader.py"),
]

def run_step(name, script):
    print(f"\n=== {name} ({script}) ===")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"❌ Step failed: {name}")
        sys.exit(result.returncode)
    print(f"✅ Finished: {name}")

if __name__ == "__main__":
    for name, script in steps:
        run_step(name, script)
    print("\n🎉 Pipeline completed successfully!")
