import os
import pickle
import json
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'z5r00script@gmail.com'


def read_json_file(file_name="email.json"):
    # Define the file path
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Read the data from the JSON file
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            dst=data.get('destination')
            subject=data.get('subject')
            message=data.get('message')
                        
            return dst,subject,message
    except FileNotFoundError:
        print(f"The file {file_name} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_name}.")
        return None


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def build_message(destination, obj, body):
    
    message = MIMEMultipart()
    message['to'] = destination
    message['From'] = our_email
    message['Subject'] = obj
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body):
    print(f'sending the body {body}\n')
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body)
    ).execute()


if __name__=='__main__':
    # get the Gmail API service
    email_=read_json_file()
    print('\n\nprinting email')
    print(email_[2])
    service = gmail_authenticate()
    send_message(service, email_[0],email_[1],email_[2])