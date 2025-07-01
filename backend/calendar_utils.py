import datetime
from typing import List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Set your calendar ID (can be found in Google Calendar settings)
CALENDAR_ID = 'primary'  # Replace with your test calendar ID if needed

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def check_availability(start_time: datetime.datetime, end_time: datetime.datetime, calendar_id: str = CALENDAR_ID) -> bool:
    service = get_calendar_service()
    body = {
        "timeMin": start_time.isoformat() + 'Z',
        "timeMax": end_time.isoformat() + 'Z',
        "items": [{"id": calendar_id}],
    }
    eventsResult = service.freebusy().query(body=body).execute()
    busy_times = eventsResult['calendars'][calendar_id]['busy']
    return len(busy_times) == 0

def create_event(
    summary: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    description: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    calendar_id: str = CALENDAR_ID
) -> dict:
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }
    if description:
        event['description'] = description
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event
