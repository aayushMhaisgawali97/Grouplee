import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText

def build_service(token_path='token.json'):
    creds = Credentials.from_authorized_user_file(token_path)
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        subject = sender = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
        snippet = msg_data.get('snippet', '')
        email_list.append({'id': msg['id'], 'subject': subject, 'sender': sender, 'snippet': snippet})
    return email_list

def get_email_body(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg['payload'].get('parts', [])
    data = ''
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            break
    if not data:
        data = msg['payload']['body']['data']
    return base64.urlsafe_b64decode(data).decode('utf-8')

def send_email(service, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    service.users().messages().send(userId='me', body=message).execute()
