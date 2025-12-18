AutoTube — Fully Automated AI YouTube Video Generator

AutoTube is an end-to-end automated pipeline that creates, edits, and uploads YouTube videos using AI.

Built entirely with Python, this system generates scripts, creates voiceovers, downloads relevant images/videos, edits them into a vertical slideshow video, generates thumbnails, and uploads the finished video to YouTube.

Designed to automate content creation at scale.


---

✨ Features

🔹 AI Content Generation

Creates script, title, description, and hashtags

Supports Ollama, Gemini, OpenAI, etc.


🔹 Human Review Stage

Lets user edit the generated script before production


🔹 AI Voiceover

Converts script to clean narration using TTS engines

Saves audio into data/voice.mp3


🔹 Media Automation

Downloads images/videos based on script topic

Uses them to create a 9:16 vertical video


🔹 Video Creation

Creates slideshow with transitions

Adds thumbnail

Uses MoviePy & ffmpeg

Supports subtitles (Whisper integration optional)


🔹 YouTube Auto Upload

Uploads the video with title, description, tags

Uses YouTube Data API v3


🔹 One-Click Pipeline

Run everything using

python pipelinerunner.py

ipeline Flow

AI Script → Review → Voiceover → Assets → Video Creation → Thumbnail → Upload


---

🛠️ Technologies Used

1.Python

2.MoviePy

3.ffmpeg

4.Google YouTube Data API

5.AI Models (deepseek / Ollama / OpenAI)

6.EndeavourOS / Arch Linux

## System Requirements
- Python 3.9+
- FFmpeg (required for video & audio processing)

Install FFmpeg:
- Ubuntu / Linux: sudo apt install ffmpeg
- Windows: https://ffmpeg.org/download.html

📁 Project Structure

AutoTube/
│
├── pipeline_runner.py
├── script_caption_hashtags_ollama.py
├── review_and_confirm.py
├── voiceover_ms.py
├── image_downloader.py
├── video_creator_advanced.py
├── youtube_uploader.py
│
├── config.py
├── data/              # stores audio, subtitles, final video, etc.
├── assets/            # images + videos used in 


How to Run

1. Clone the repo

git clone https://github.com/<your-username>/AutoTube.git
cd AutoTube

2. Create virtual env

python -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run full pipeline

python pipeline2.py

🔐 YouTube API Setup (Required for Upload)

This project uses the YouTube Data API v3 to upload videos.
Follow the steps below to configure it.

1️⃣ Create Google Developer Account

Go to 👉 https://console.cloud.google.com/

Sign in with your Google account

Create a new project

2️⃣ Enable YouTube Data API

In Google Cloud Console, go to APIs & Services → Library

Search for YouTube Data API v3

Click Enable

3️⃣ Create OAuth Credentials

Go to APIs & Services → Credentials

Click Create Credentials → OAuth Client ID

If prompted, configure OAuth Consent Screen:

User type: External

App name: Any name (e.g., AutoTube)

Save and continue

Application type: Desktop App

Create the credential

Download the JSON file

4️⃣ Add Credentials to Project

Rename the downloaded file to:

client_secret.json


Place it in the root directory of the project

⚠️ Do not upload client_secret.json to GitHub

5️⃣ Authenticate YouTube Account

When you run the uploader for the first time:

python youtube_uploader.py


A browser window will open

Sign in to your YouTube account

Grant permissions

This will generate a token.json file automatically.

⚠️ Do not upload token.json to GitHub

6️⃣ Run the Pipeline

After setup, run the pipeline in order:

python pipeline_runner.py


🎯 Why I Built This

To challenge myself and learn:

AI automation

Python pipelines

Real-world API integration

Video processing

End-to-end project development


This project demonstrates software engineering + AI expertise.


---

🤝 Contributions

Feel free to fork this project and suggest improvements!


---

📬 Contact

If you're an HR or recruiter, I’m currently seeking Internship Opportunities in:

AI/ML

Python Development

Full Stack

Automation

Cloud Engineering
