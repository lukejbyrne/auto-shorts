import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import os
import datetime
import pytz
import googleapiclient

# Set the path to your client secrets file
CLIENT_SECRETS_FILE = "creds/client_secret_948207109811-i3ctl7umji7e4632koo41f8pki8545qo.apps.googleusercontent.com.json"

# Set the path to your video file
VIDEO_FILE_1 = "final/my_video_with_absolute.png_logo.mp4"
VIDEO_FILE_2 = "final/my_video_with_inspire.png_logo.mp4"
VIDEO_FILE_3 = "final/my_video_with_measured.png_logo.mp4"
VIDEO_FILE_4 = "final/my_video_with_motivate.png_logo.mp4"
VIDEO_FILE_5 = "final/my_video_with_raw.png_logo.mp4"
VIDEO_FILE_6 = "final/my_video_with_succeed.png_logo.mp4"

# Set the YouTube API service name and version
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Set the desired time zone (in this case, GMT)
TIMEZONE = pytz.timezone('GMT')

# Define the start time for the videos (tomorrow at 1pm GMT)
now = datetime.datetime.now(TIMEZONE)
start_time = now.replace(hour=13, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

# Set the paths to the credentials files
CREDENTIALS_FILES = ["youtube_credentials1.json", "youtube_credentials2.json", "youtube_credentials3.json", "youtube_credentials4.json", "youtube_credentials5.json", "youtube_credentials6.json"]

# Set the scopes for the API
API_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Set the port for the local server
LOCAL_SERVER_PORT = 8079

# Define titles for each video
# Absolute - DareTo Inspire - Measured - DareTo Motivate - Raw - DareTo Succeed
titles = ["Unlocking Success by Waking Up Before the World | Jocko Willink",
          "SEAL Team Secrets: How Top Performers Stay Ahead and Get Things Done | Jocko Willink",
          "Setting Boundaries and Finding Time for What Matters | Jocko Willink",
          "The Secret to Getting Stuff Done | Jocko Willink",
          "Efficiency Hacks: Morning Routines of High Achievers | Jocko Willink"
]

# Get the credentials for each channel
credentials = []
youtube = []

for i, credentials_file in enumerate(CREDENTIALS_FILES):
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as f:
            credentials.append(google.oauth2.credentials.Credentials.from_authorized_user_info(json.loads(f.read())))
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, API_SCOPES)
        credentials.append(flow.run_local_server(port=LOCAL_SERVER_PORT))
        with open(credentials_file, "w") as f:
            f.write(credentials[-1].to_json())

    youtube.append(build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials[i]))

# Loop through each channel and upload a video
for i in range(1, 7):
    # Use cached credentials for the channel
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials[i-1])

    # Define the metadata for the video
    request_body = {
        "snippet": {
            "title": titles[i-1],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
            # "publishAt": start_time.isoformat()
        }
    }

    # Upload the video to the channel
    video_file = locals()[f"VIDEO_FILE_{i}"]  # Get the video file path
    print("asdfqasfvbdewdsvedsv: ", video_file)
    media_file = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    print("Video {} scheduled. Video ID: {}".format(i, response["id"]))