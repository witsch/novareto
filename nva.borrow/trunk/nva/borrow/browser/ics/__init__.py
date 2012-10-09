import os
from datetime import datetime, date, timedelta
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


HOLIDAYS = getHolidays()

def firstWorkDayAfter(dt, day_offset=0):

    assert isinstance(dt, date)
    candidates = list()
    for days in range(7):           
        new_dt = dt + timedelta(days=day_offset+days)

        # check for holidays#
        if new_dt in HOLIDAYS:
            continue
        # weekend
        if new_dt.isoweekday() in [6,7]:
            continue
        print new_dt
        return new_dt


if __name__ == '__main__':
    print getHolidays()
    print firstWorkDayAfter(datetime.now().date(), 10)
