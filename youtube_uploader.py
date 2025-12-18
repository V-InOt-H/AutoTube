import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# -----------------------------
# YouTube service
# -----------------------------
def get_service():
    if not os.path.exists("token.json"):
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    else:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    return build("youtube", "v3", credentials=creds)

# -----------------------------
# Main uploader
# -----------------------------
def main():
    youtube = get_service()

    # Load metadata
    with open("data/title.txt") as f:
        title = f.read().strip()

    with open("data/description.txt") as f:
        desc = f.read().strip()

    with open("data/hashtags.txt") as f:
        hashtags = f.read().strip()

    full_description = f"{desc}\n\n{hashtags}"

    # ✅ FIX: Always upload latest video
    video_path = "assets/latest_video/final.mp4"

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            "Latest video not found. Run video_creator_advanced.py first."
        )

    print("⬆️ Uploading video:", video_path)

    upload_request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": full_description,
                "categoryId": "28",  # Science & Technology
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path, resumable=True)
    )

    response = upload_request.execute()
    video_id = response["id"]

    print(f"✅ Video uploaded successfully! Video ID: {video_id}")

    # Thumbnail (optional)
    thumb_path = "assets/images/thumbnail.jpg"
    if os.path.exists(thumb_path):
        print("🖼 Uploading thumbnail...")
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=thumb_path
        ).execute()

    print("🚀 Upload complete.")

# -----------------------------
if __name__ == "__main__":
    main()
