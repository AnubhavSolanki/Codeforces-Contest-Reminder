from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('calendar', 'v3', credentials=creds)
result = service.calendarList().list().execute()
calendar_id = result['items'][3]['id']

def reminder(contest_name,start_time,end_time):
    time_zone = 'Asia/Kolkata'
    event = {
    'summary': contest_name,
    'location': 'Dehradun',
    'description': 'Codeforces Contest',
    'start': {
        'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S') ,
        'timeZone': time_zone,
    },
    'end': {
        'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': time_zone,
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    service.events().insert(calendarId = calendar_id,body = event).execute()
