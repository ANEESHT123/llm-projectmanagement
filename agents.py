from crewai import Agent, Crew, Task
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from datetime import datetime, timedelta, time
import pytz

os.environ["OPENAI_API_KEY"] = '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'

# Google API Credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'iron-inkwell-401009-0e16ca2f16de.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Function to schedule meeting time in IST
def get_meeting_time():
    """Schedule a meeting at 10 AM IST on the next available weekday."""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    next_meeting_day = now.date()
    
    if now.time() >= time(10, 0):
        next_meeting_day += timedelta(days=1)
    
    while next_meeting_day.weekday() >= 5:
        next_meeting_day += timedelta(days=1)
    
    start_time_ist = ist.localize(datetime.combine(next_meeting_day, time(10, 0)))
    end_time_ist = start_time_ist + timedelta(hours=1)
    
    return start_time_ist.isoformat(), end_time_ist.isoformat()

# Function to create a Google Calendar event
def create_event():
    """Creates a Google Calendar event in IST timezone."""
    try:
        service = build('calendar', 'v3', credentials=credentials)
        start_time, end_time = get_meeting_time()
        
        event = {
            'summary': "Scheduled Meeting",
            'description': "Automated meeting scheduled by CrewAI.",
            'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
        }
        calendarId= "aneesht240@gmail.com"
        event = service.events().insert(calendarId=calendarId, body=event).execute()
        print(f"✅ Event Created: {event.get('htmlLink', 'No Link')}")
        return f"✅ Event Created: {event.get('htmlLink', 'No Link')}"
    except Exception as e:
        print(f"❌ Error Creating Event: {str(e)}")
        return f"❌ Error Creating Event: {str(e)}"

# CrewAI Agent and Task
scheduler_agent = Agent(
    role="Meeting Scheduler",
    goal="Schedule meetings in Google Calendar automatically.",
    backstory="An assistant that manages your schedule effortlessly.",
    verbose=True
)

schedule_meeting_task = Task(
    description="Schedule a meeting on Google Calendar in IST timezone.",
    agent=scheduler_agent,
    expected_output="A Google Calendar event scheduled at 10 AM IST.",
    function=create_event
)

crew = Crew(
    name="Meeting Scheduler Crew",
    agents=[scheduler_agent],
    tasks=[schedule_meeting_task]
)

if __name__ == "__main__":
    print(crew.kickoff())
