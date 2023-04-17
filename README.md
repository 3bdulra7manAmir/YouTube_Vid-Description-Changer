![image](https://user-images.githubusercontent.com/64253660/232464382-73c13477-81f6-44ba-b913-c891a47e8a20.png)

<hr style="border-radius: 2%; margin-top: 60px; margin-bottom: 60px;" noshade="" size="20" width="100%">

# Features

-   Replace the Text of a Specific line or more than one line by The words you want!

# Usage

1. install all required Libraries.
  .os
  .re
  .google_auth_oauthlib
  .googleapiclient
  .google.auth.transport.requests
  .google.oauth2.credentials
  .google_auth_oauthlib.flow
  .googleapiclient.errors

2. Replace the API KEY with your KEY.
  api_key = "Your API KEY"
  
3. Replace the Auth Json file path with your File path.
  client_secrets_file = "Path in Here"

4. Replce the lines.
  old_lines = ["^^^^^^^", "^^^^^^^"]
  new_lines = ["^^^^^^^", "^^^^^^^"]

5. in "flow = InstalledAppFlow.from_client_secrets_file" put your Auth Json file path again.
  ("Path in Here", scopes)
