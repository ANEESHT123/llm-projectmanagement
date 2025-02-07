# agents/scheduling_agent.py

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import datetime
import os

class SchedulingAgent:
    def __init__(self, google_service):
        self.google_service = google_service

    def check_availability(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.google_service.events().list(calendarId='primary', timeMin=now,
                                                          maxResults=10, singleEvents=True,
                                                          orderBy='startTime').execute()
        events = events_result.get('items', [])
        busy_slots = [event['start']['dateTime'] for event in events]
        return busy_slots

    def propose_meeting(self, proposed_time):
        busy_slots = self.check_availability()
        if proposed_time not in busy_slots:
            return f"Meeting scheduled for {proposed_time}"
        else:
            return f"Sorry, that time is taken. Please suggest another time."
