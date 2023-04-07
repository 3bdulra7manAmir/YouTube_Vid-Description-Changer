import os
import os.path

import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyC5lLd1CMhXwEBR37hSX1JWWGt_3dkb9AM"
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "D:\\Projects\\PyCharm\\YouTube_API_Description\\client_secret_92936865464-f9cpbdctpcum6c32ivdi87nsfh8f7o0d.apps.googleusercontent.com.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

        request = youtube.videos().update(
        part="snippet",
        body={
            "id": "vLAd3etnbww",
            "snippet": {
                "title": "Mw2 CR No Loose Ends a Slightly Different end.",
                "categoryId": 20,
                "description": "aaaaaaaaaaaa",
                    },
                }
            )
        response = request.execute()
        print(response)
    except HttpError as error:
            print(f'An HTTP error {error.resp.status} occurred:\n{error.content}')

main()
