# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
from Products.CMFCore.utils import getToolByName
from uv.bsbetreuung import bsbetreuungMessageFactory as _


def portal_catalog(context):
    return getToolByName(context, 'portal_catalog')

def getFragenInOrder(context):
    pcat = portal_catalog(context)
    brains = pcat(portal_type = 'Fragestellung', review_state='published', show_inactive=True)
    objects = [x.getObject() for x in brains]
    objects.sort(key=lambda x: x.getOrder(), reverse=False)
    return objects

def formatFragen(context):
    pcat = portal_catalog(context)
    brains = pcat(portal_type = 'Fragestellung', review_state='published', show_inactive=True)
    fragen = {}
    for i in brains:
        mydict = {}
        frage = i.getObject()
        mydict['title'] = frage.Title()
        mydict['fieldtype'] = frage.getFieldtype()
        optionen = {}
        if frage.getFieldtype() == 'choice':
            for j in frage.getOptionen():
                option = j.split('|')
                optionen[option[0]] = option[1]
        mydict['optionen'] = optionen
        fragen[frage.id] = mydict
    return fragen


def formatAufgaben(context):
    pcat = portal_catalog(context)
    brains = pcat(portal_type = 'Aufgabe', review_state='published', show_inactive=True)
    aufgaben = {}
    for i in brains:
        aufgabe = i.getObject()
        aufgaben[aufgabe.getNummer()] = aufgabe.Title()
    return aufgaben

def formatFloat(value):
    valuestring = "%.1f" %value
    valuestring = valuestring.replace('.',',')
    return valuestring
