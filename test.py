import os.path
import re

import google_auth_oauthlib
import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

client_secrets_file = "D:\\Projects\\PyCharm\\YouTube_API_Description\\client_secret_92936865464-f9cpbdctpcum6c32ivdi87nsfh8f7o0d.apps.googleusercontent.com.json"
scopes = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyC5lLd1CMhXwEBR37hSX1JWWGt_3dkb9AM"
SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
x = 0

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "D:\\Projects\\PyCharm\\YouTube_API_Description\\client_secret_92936865464-f9cpbdctpcum6c32ivdi87nsfh8f7o0d.apps.googleusercontent.com.json",
            SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

old_line = 'https://discord.gg/seGhsz3'
new_line = 'https://discord.gg/CHZea8zvBG'

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=creds)

try:
    # get the channel ID for the authenticated user
    channels_list_response = youtube.channels().list(
        part="id",
        id="UCG7Whchg17wl-CslGSaFKWw",
    ).execute()
    print(channels_list_response)

    # get the uploads playlist ID for the channel
    channel_id = channels_list_response['items'][0]['id']
    playlist_response = youtube.playlists().list(
        channelId=channel_id,
        part='id',
        maxResults=1
    ).execute()
    print(channel_id)
    print(playlist_response)

    uploads_playlist_id = playlist_response['items'][0]['id']

    # get the video IDs for the channel's uploaded videos
    playlist_items_response = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part='id,snippet',
        maxResults=100
    ).execute()

    while playlist_items_response:
        # iterate through each video and update its description
        for item in playlist_items_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet'
            ).execute()
            video_description = video_response['items'][0]['snippet']['description']
            new_description = re.sub(old_line, new_line, video_description)
except HttpError as error:
    print(f'An HTTP error {error.resp.status} occurred:\n{error.content}')
