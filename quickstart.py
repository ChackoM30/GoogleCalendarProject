from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def createNewEvent(service):
    summ = input("Enter summary: ")
    describe = input("Enter description: ")
    begin_day = input("Enter start day(YYYY-MM-DD): ")
    begin_time = input("Enter start time(HH:MM:SS; military time): ")
    end_day = input("Enter end day(YYYY-MM-DD): ")
    end_time = input("Enter end time(HH:MM:SS; military-time): ")
    locate = input("Enter location: ")
    begin = begin_day + "T" + begin_time + "-05:00"
    end = end_day + "T" + end_time + "-05:00"
    event = {

    'summary': summ,
    'description': describe,
    'location': locate,
    'start': {
      'dateTime': begin,
    },
    'end': {
      'dateTime': end,
    },
  }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created!')
    main()

def showNextEvents(service):
    """
    Prints the start and name of the next events on the user's calendar.
    """
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    num_events = input('How many events would you like to see?')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=int(num_events), singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        #Parses data to give formatted metadata
        start = event['start'].get('dateTime', event['start'].get('date'))
        date = start[0:10]
        time = start[11:19]
        print("Name of event: " + event['summary'])
        print("Date of event: " + date)
        print("Time of event: " + time)
        print("")
    main()

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    #Determines if user wants to access or create events
    choice = input("Press A to access events, press C to create an event, press E to exit ")
    if choice == "A" or choice == "a":
        showNextEvents(service)
    elif choice == "C" or choice == "c":
        createNewEvent(service)
    elif choice == "E" or choice == "e":
        exit()

if __name__ == '__main__':
    main()
