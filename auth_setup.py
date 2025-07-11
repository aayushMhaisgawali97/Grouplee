from google_auth_oauthlib.flow import InstalledAppFlow

# Define the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    # Load credentials and create flow
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the access token in token.json
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("✅ token.json created successfully.")

if __name__ == '__main__':
    main()
