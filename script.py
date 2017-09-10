try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import string
import quickstart
import httplib2
from apiclient import discovery
from oauth2client import tools
import datetime
import base64
from autocorrect import spell
import re

def grabContent(string):
    string = string.splitlines()
    #for events
    frequency = "RRULE:FREQ=DAILY"
    time = "10"
    description = ""

    events = []

    titlearray = ["take", "daily", "bedtime", "every", "needed", "mouth", "hours", "capsule", "tablespoon", "days", "up to", "one"]

    for i in string:
        print(i)
        i = re.sub(r'([^\s\w]|_)+', '', i)
        print(i, "/n")
        if any(word in i.lower() for word in titlearray):
            description += i
    twotime = ['twice']
    threetime = ['times', '3', 'a day', "8", ]
    fourtime = ['6']
    night = ['night', 'bedtime']
    tendays = ['10']

    #TWO TIMES
    if any(word in description.lower() for word in twotime):
      events.append(getEvent(description, "08", frequency))
      events.append(getEvent(description, "20", frequency))
    #THREE TIMES
    elif any(word in description.lower() for word in threetime):
      events.append(getEvent(description, "08", frequency))
      events.append(getEvent(description, "14", frequency))
      events.append(getEvent(description, "20", frequency))
      if '10' in description.lower():
        frequency = "RRULE:FREQ=DAILY;COUNT=10"
    #FOUR TIMES
    elif any(word in description.lower() for word in fourtime):
      events.append(getEvent(description, "08", frequency))
      events.append(getEvent(description, "13", frequency))
      events.append(getEvent(description, "18", frequency))
      events.append(getEvent(description, "23", frequency))
    #AT NIGHT
    elif any(word in description.lower() for word in night):
      description = "TAKE ONE TABLET EVERY NIGHT AT BEDTIME"
      events.append(getEvent(description, "22", frequency)) 
    else:
      if len(description) < 10:
        description = "TAKE ONE TABLET"
      events.append(getEvent(description, "08", frequency))

    print(description)
    return events

def getEvent(description, time, frequency):
    time = int(time) - 6
    starttime = "2017-09-10T" + str(time) + ":00:00-10:00"
    endtime = "2017-09-10T" + str(time+1) + ":00:00-10:00"
    event = {
      'summary': description,
      'description': 'Take your prescription pills',
      'start': {
        'dateTime': starttime,
        'timeZone': 'EST',
      },
      'end': {
        'dateTime': endtime,
        'timeZone': 'EST',
      },
      'recurrence': [
        frequency
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    return event

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = quickstart.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    string = pytesseract.image_to_string(Image.open('test.jpg'))

    events = grabContent(string)

    for event in events:
      event = service.events().insert(calendarId='primary', body=event).execute()
      print('Event created:', event.get('htmlLink'))
      print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == '__main__':
    main()
