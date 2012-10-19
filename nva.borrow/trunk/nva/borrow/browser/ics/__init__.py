import os
import collections
from datetime import datetime, date, timedelta
import glob
import icalendar

MONTH_NAMES = [
'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun',
'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'
]

DAY_NAMES = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']


class myDate(date):
    def __new__(cls, dt, is_holiday=False, text=''):
        new_dt = date.__new__(cls, dt.year, dt.month, dt.day)
        new_dt.weekday_name = DAY_NAMES[new_dt.weekday()]
        new_dt.is_holiday = is_holiday
        new_dt.text = text
        new_dt.week = new_dt.isocalendar()[1]
        return new_dt

def getHolidays():

    events = dict()
    for ics in glob.glob('%s%s*.ics' % (os.path.dirname(__file__), os.path.sep)):
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
        return new_dt

def getDateRange(dt, num_days=30):
    MM_YY = collections.namedtuple('MMYY', 'month year, monthname')

    result = dict(dates=list(), 
                  dates_iso=list(),
                  months=list(), 
                  month_year=dict())

    for day in range(num_days):

        current_ = dt + timedelta(days=day)

        text = ''
        if current_.date() in HOLIDAYS:
            text = HOLIDAYS[current_.date()].rsplit('Alle', 1)[0]
        current = myDate(current_, 
                         text=text,
                         is_holiday=(current_.date() in HOLIDAYS))

        # weekend
        if current.isoweekday() in [6,7]: 
            continue

        # store date native
        result['dates'].append(current)
        result['dates_iso'].append(current.isoformat())

        mm_yy = MM_YY(month=current.month, year=current.year, monthname=MONTH_NAMES[current.month-1])
        if not mm_yy in result['months']:
            result['months'].append(mm_yy)

        # store date by month+year
        if not mm_yy in result['month_year']:
            result['month_year'][mm_yy] = list()
        result['month_year'][mm_yy].append(current)

    return result

def nextMonths(num_month=12):
    """ Return a data structure for the next N months """

    now = datetime.now().date().replace(day=1)
    result = list()
    for i in range(1, num_month+1):
        current = (now + timedelta(days=i*28)).replace(day=1)
        result.append(dict(month=current.month,
                           year=current.year,
                           date=current.isoformat(),
                           month_name=MONTH_NAMES[current.month-1]))

    return result

if __name__ == '__main__':
    print getHolidays()
    print firstWorkDayAfter(datetime.now().date(), 10)
    print getDateRange(datetime.now().date(), 60)



