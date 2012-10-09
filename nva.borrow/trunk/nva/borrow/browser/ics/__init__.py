import os
import glob
import icalendar

def getHolidays():

    events = dict()
    for ics in glob.glob('%s%s*.ics' % (os.path.dirname(__file__), os.path.sep)):
        print ics
        cal = icalendar.Calendar.from_ical(open(ics,'rb').read())
        for item in cal.walk():
            if isinstance(item, icalendar.cal.Event):
                desc = item['DESCRIPTION'].to_ical()
                start = item['DTSTART'].dt
                end = item['DTEND'].dt
                events[start] = desc
    return events

if __name__ == '__main__':
    print getHolidays()
