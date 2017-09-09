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

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
string = pytesseract.image_to_string(Image.open('image.jpg'))

def grabContent(string):
	string = string.splitlines()
	description = ""
	title = ""
	for i in string:
		if "TAKE" in i:
			description += i
		elif "UP" in i:
			description += i
		elif "MG TABLETS" in i:
			title = i
	print(title)
	print(description)

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    grabContent(string)
    credentials = quickstart.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
