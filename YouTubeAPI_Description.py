import os.path
import re
import google_auth_oauthlib
import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

api_key = "AIzaSyC5lLd1CMhXwEBR37hSX1JWWGt_3dkb9AM"  # "My YouTube API Access KEY"
client_secrets_file = "D:\\Projects\\PyCharm\\YouTube_API_Description\\client_secret_92936865464-f9cpbdctpcum6c32ivdi87nsfh8f7o0d.apps.googleusercontent.com.json"  # "Path to Client Auth Json file"
api_service_name = "youtube"  # "service name gdrive etc"
api_version = "v3"  # "API Version"
scopes = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # here

# "Enter the lines you want it to be replaced"
old_lines = ["https://discord.gg/seGhsz3", """Discord Account:
Shadow#1942"""]

# "Enter the new lines that will replace the old ones"
new_lines = ["https://discord.gg/CHZea8zvBG", ""]

# "Authenticate and build the YouTube API client"   # You are Authorized
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

creds = None   # init Value
if os.path.exists('token.json'):  # "Received Access Token file"
    creds = Credentials.from_authorized_user_file('token.json', scopes)  # here

if not creds or not creds.valid:  # "if no Access Token received Then Try Again"
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())  # "Try Again code line"
    else:
        flow = InstalledAppFlow.from_client_secrets_file(  # here
            "D:\\Projects\\PyCharm\\YouTube_API_Description\\client_secret_92936865464-f9cpbdctpcum6c32ivdi87nsfh8f7o0d.apps.googleusercontent.com.json",
            scopes)
        creds = flow.run_local_server(port=0)  # here
    with open('token.json', 'w') as token:  # "if Access Token Received Save it"
        token.write(creds.to_json())

youtube = googleapiclient.discovery.build(  # here
    api_service_name, api_version, credentials=creds)

try:
    # "Retrieve a list of all the videos in your channel"
    channels_response = youtube.channels().list(part="contentDetails", mine=True).execute()  # "Return Channel videos List"
    channel_id = channels_response["items"][0]["id"]  # "Requests Channel ID"
    playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]  # All videos in play list
    videos = []  # a Videos List for saving info
    next_page_token = None  # here

    while True:
        playlist_items_response = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=111,
                                                               pageToken=next_page_token).execute()
        videos += playlist_items_response["items"]
        next_page_token = playlist_items_response.get("nextPageToken")
        if not next_page_token:  # "if there are no more pages then get out"
            break

    # Loop through all the videos and replace the specified lines in the description
    for video in videos:  # ""
        video_id = video["snippet"]["resourceId"]["videoId"]  # ""
        video_title = video["snippet"]["title"]  # ""
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()  # ""
        description = video_response["items"][0]["snippet"]["description"]  # ""
        for i in range(len(old_lines)):  # ""
            description = re.sub(old_lines[i], new_lines[i], description)  # ""
        youtube.videos().update(part="snippet",
                                body={"id": video_id, "snippet": {"description": description, "categoryId": 20, "title": video_title}}).execute()  # ""
        print("Updated description for video ID:", video_id)

except HttpError as error:
    print("An HTTP error %d occurred:\n%s" % (error.resp.status, error.content))
