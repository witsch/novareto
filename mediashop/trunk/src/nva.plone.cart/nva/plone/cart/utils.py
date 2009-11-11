# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage

def flash(request, message, type='info'):
    IStatusMessage(request).addStatusMessage(message, type=type)
