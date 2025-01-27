import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import pickle
from datetime import datetime, timedelta, timezone




def get_authenticated_service():
    """
    Handles the OAuth 2.0 flow and returns an authenticated YouTube API client.
    """
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None

    # Load existing credentials if available
    if os.path.exists("keys/token.pickle"):
        with open("keys/token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)

    # If no valid credentials are available, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ensure credentials.json exists and is correctly formatted
            flow = InstalledAppFlow.from_client_secrets_file(
                "keys/ai-slop-google-yt-key.json", SCOPES
            )
            creds = flow.run_local_server(port=0, prompt="consent")

        # Save the credentials for future runs
        with open("keys/token.pickle", "wb") as token_file:
            pickle.dump(creds, token_file)

    return build("youtube", "v3", credentials=creds)

tags = ["creepy", "horror", "shorts", "storytime","entertainment"]

def upload_to_youtube(video_file, title, description, tags, category_id="24", privacy_status="private", publish_after_days=1):
    """
    Uploads an MP4 video to YouTube as a Short.

    Args:
        video_file (str): Path to the video file.
        title (str): Title of the video.
        description (str): Description of the video.
        tags (list): List of tags for the video.
        category_id (str): YouTube category ID (default: "24" for Entertainment).
        privacy_status (str): Privacy status (e.g., "public", "unlisted", "private").
    """
    youtube = get_authenticated_service()

    publish_time = (datetime.now(timezone.utc) + timedelta(days=publish_after_days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"Publishing video at {publish_time}")

    # Prepare video metadata
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status,
            'publishAt': publish_time,
            'madeForKids': False  # Set to True if the video is for kids
        }
    }

    # Upload video
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")

    return (f"Upload Complete! URL: https://www.youtube.com/shorts/{response['id']}")


if __name__ == "__main__":
    # video_file = "creepy_story_video.mp4"  # Replace with your video file
    # title = "Creepy Story Short TESTING FROM DESKTOP"
    # description = "A spine-chilling tale to keep you up at night."
    # tags = ["creepy", "horror", "shorts", "storytime"]
    
    # # Call the function to upload the video
    # upload_to_youtube(video_file, title, description, tags, privacy_status="unlisted")
    pass