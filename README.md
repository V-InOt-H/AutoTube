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


📁 Project Structure

AutoTube/
│
├── pipeline2.py
├── script_caption_hashtags_ollama.py
├── review_and_confirm.py
├── voiceover_ms.py
├── image_downloader.py
├── video_creator_advanced.py
├── thumbnail_generator.py
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
