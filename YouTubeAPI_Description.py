import os
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = "path/to/client_secrets.json"  # Update this path
TOKEN_FILE = "token.json"

# Replace lines in descriptions
OLD_LINES = ["https://discord.gg/seGhsz3", "Discord Account:\nShadow#1942"]
NEW_LINES = ["https://discord.gg/CHZea8zvBG", ""]


def authenticate_youtube_api():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or reauthenticate if credentials are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def get_channel_videos(youtube):
    try:
        # Get channel details
        channels_response = youtube.channels().list(part="contentDetails", mine=True).execute()
        uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Retrieve all videos in the uploads playlist
        videos = []
        next_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            videos.extend(playlist_items_response["items"])
            next_page_token = playlist_items_response.get("nextPageToken")
            if not next_page_token:
                break
        return videos
    except HttpError as error:
        print(f"An HTTP error occurred: {error}")
        return []


def update_video_description(youtube, video_id, title, description):
    try:
        youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": title,
                    "description": description,
                    "categoryId": 20
                }
            }
        ).execute()
        print(f"Updated description for video ID: {video_id}")
    except HttpError as error:
        print(f"Failed to update video ID {video_id}: {error}")


def main():
    # Authenticate and initialize the YouTube API client
    youtube = authenticate_youtube_api()

    # Get all videos from the user's channel
    videos = get_channel_videos(youtube)

    # Update the descriptions of each video
    for video in videos:
        video_id = video["snippet"]["resourceId"]["videoId"]
        title = video["snippet"]["title"]

        # Get the current description
        video_details = youtube.videos().list(part="snippet", id=video_id).execute()
        current_description = video_details["items"][0]["snippet"]["description"]

        # Replace old lines with new ones
        updated_description = current_description
        for old_line, new_line in zip(OLD_LINES, NEW_LINES):
            updated_description = re.sub(re.escape(old_line), new_line, updated_description)

        # Only update if the description has changed
        if current_description != updated_description:
            update_video_description(youtube, video_id, title, updated_description)


if __name__ == "__main__":
    main()
