# -*- coding: utf-8 -*-

import datetime
import DateTime
import calendar
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CalendarView(BrowserView):

    minmax = 5

    index = ViewPageTemplateFile("calendar.pt")
    
    def events(self, start, end):
        """Get the search results
        """
        date_range_query = {'query': (start, end), 'range': 'min:max'}

        context = aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        folder_path = '/'.join(context.getPhysicalPath())
        for brain in portal_catalog.searchResults(
            sort_on='start',
            start=date_range_query,
            portal_type='Event',
            review_state='published',
            path={'query': folder_path, 'depth': 1}):
            yield brain

    @staticmethod
    def get_month_name(month):
        return calendar.month_name[month]

    def sort_time(self, year, today):
        events = {}

        today = DateTime.DateTime(today)
        start = DateTime.DateTime(datetime.datetime(
            year=year, month=1, day =1))
        end = DateTime.DateTime(datetime.datetime(
            year=year, month=12, day=31, hour=23, minute=59, second=59))

        for event in self.events(start, end):
            event_start = event['start']
            event_end = event['end']
            month = event_start.month()
            events_list = events.setdefault(month, [])
            if event_start > today:
                struct = ('upcoming', event)
            elif event_end < today:
                struct = ('finished', event)
            elif event_start <= today <= event_end:
                struct = ('current', event)
            events_list.append(struct)
        return events

    def update(self):
        today = datetime.datetime.now()
        default = today.year
        limit_previous = default - self.minmax
        limit_next = default + self.minmax
        year = int(self.request.form.get('year', default))
        if not limit_previous <= year <= limit_next:
            self.overflow = True
        else:
            self.overflow = False
            self.events = self.sort_time(year=year, today=today)

        self.current_year = year
        self.next_year = limit_next > year and year + 1 or None
        self.previous_year = limit_previous < year and year - 1 or None

    def render(self):
        return self.index()

    def __call__(self, *args, **kwargs):
        self.update()
        return self.render()
