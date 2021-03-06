from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
from assignment import Assignment
from consts import *
from time_ import Time

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar.events']


def export(assignments, user):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    evs = [assignment_to_event(ass, user) for ass in assignments]

    creds = None
    # cc
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('google_api/token.json'):
        creds = Credentials.from_authorized_user_file('google_api/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('google_api/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # # Call the Calendar API
        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # events_result = service.events().list(calendarId='primary', timeMin=now,
        #                                       maxResults=10, singleEvents=True,
        #                                       orderBy='startTime').execute()
        # events = events_result.get('items', [])

        for event in evs:
            service.events().insert(calendarId='primary', body=event).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


def assignment_to_event(ass: Assignment, user):
    summary = ass.get_name()
    start, end = ass.to_datetime_time()
    participants = ass.get_participants()
    kind = (ass.get_kind())

    event = {
        'summary': summary,
        'colorId': str(GOOGLE_COLORS[kind]),
        'start': {
                'dateTime': start.astimezone().isoformat(),
        },
        'end': {
                'dateTime': end.astimezone().isoformat(),
        },
    }

    event['attendees'] = []
    event['attendees'].append({'email': user.get_name() + "@gmail.com"})
    if participants:
        for participant in participants:
            if participant != user:
                event['attendees'].append({'email':participant.get_name() + "@gmail.com"})
    return event

if __name__ == '__main__':
    b1 = Assignment(week=1, name="m1", duration=Time(h=2), kind=kinds["MEETING"], participants=["ophir.carmel"], day=4,
                    time=Time(h=20, m=00))
    b2 = Assignment(week=1, name="m2", duration=Time(h=3), kind=kinds["TASK"], participants=["ophir.carmel"], day=5,
                    time=Time(h=13, m=30))

    export([b1, b2])
