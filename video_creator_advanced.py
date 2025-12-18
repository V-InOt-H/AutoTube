import os
import glob
import subprocess
import shutil
from moviepy import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips
)

# Directories
IMAGES_DIR = "assets/images"
DATA_DIR = "data"
VIDEOS_DIR = "assets/videos"
LATEST_DIR = "assets/latest_video"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(LATEST_DIR, exist_ok=True)

# -----------------------------
# Load images
# -----------------------------
def load_images():
    patterns = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(IMAGES_DIR, p)))

    files = sorted(files)
    if not files:
        raise FileNotFoundError(
            f"No images found in {IMAGES_DIR}. Run image_downloader.py first."
        )
    return files

# -----------------------------
# Process audio
# -----------------------------
def process_audio():
    raw_audio = os.path.join(DATA_DIR, "voice.mp3")
    processed_audio = os.path.join(DATA_DIR, "voice_processed.mp3")

    if not os.path.exists(raw_audio):
        raise FileNotFoundError("data/voice.mp3 not found. Run voiceover first.")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", raw_audio,
        "-filter:a", "atempo=0.9",
        processed_audio
    ]

    print("🎧 Processing audio with ffmpeg...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="ignore"))

    return processed_audio

# -----------------------------
# Main video creator
# -----------------------------
def main():
    # 1. Audio
    audio_path = process_audio()
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 2. Images
    image_files = load_images()
    per_image = duration / max(len(image_files), 1)

    width, height = 1080, 1920
    clips = []

    for img in image_files:
        clip = (
            ImageClip(img)
            .resized(height=height)
            .with_duration(per_image)
        )
        clips.append(clip)

    base_video = concatenate_videoclips(clips, method="compose")
    final_video = CompositeVideoClip([base_video]).with_audio(audio)

    # 3. Output paths
    output_video_path = os.path.join(
        VIDEOS_DIR,
        "video_output.mp4"
    )

    # 4. Write video
    final_video.write_videofile(
        output_video_path,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    # 5. Update latest video
    latest_video_path = os.path.join(LATEST_DIR, "final.mp4")
    shutil.copy(output_video_path, latest_video_path)

    print("✅ Latest video updated:", latest_video_path)
    print("🎬 Video created successfully:", output_video_path)

if __name__ == "__main__":
    main()
