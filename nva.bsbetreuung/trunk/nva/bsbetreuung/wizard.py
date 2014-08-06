# -*- coding: utf-8 -*-
from collective.beaker.interfaces import ISession

def getStep(doclist, docid, direction):
    """
    ermittelt den Listenindex fuer den naechsten Step
    """
    stepindex = doclist.index(docid)
    if direction == 'forward':
        if stepindex + 1 == len(doclist):
            return 'redir'
        return stepindex + 1
    elif direction == 'backward':
        if stepindex == 0:
            return 'redir'
        return stepindex -1


def prepareData(fragen):
    """ 
    Die Fragen werden analysiert ob es sich dabei
    um Auswahlfragen oder Floats handelt. Kommentare
    werden in separaten Listen erfasst.
    """
    valuedata = []#Lesen des Session-Cookies in dem alle Auswahlfragen Floats gespeichert werden
    commentdata = []#Lesen des Session-Cookies in dem alle Bemerkungsfragen erfasst werden
    for i in fragen:
        if i.fieldtype in ['choice', 'float'] and i.id not in valuedata:
            valuedata.append(i.id)
        elif i.fieldtype in ['textline', 'text'] and i.id not in commentdata:
            commentdata.append(i.id)
    return (valuedata, commentdata)


def getSessionCookie(context, request):
    """
    Liest das SessionCookie
    """
    session = ISession(request)
    sb_default = {'sbsum':0.0, 'sbvalues':[], 'steps':[], 'stepdata':{}}
    cookie = session.get('sb', sb_default)
    data_startseite = session.get('start', {})
    mitarbeiter = data_startseite.get('mitarbeiter', 0.0)
    if isinstance(mitarbeiter, str) or isinstance(mitarbeiter, unicode):
        mitarbeiter = float(str(mitarbeiter).replace(',','.'))
    return (cookie, mitarbeiter)


def setSessionCookie(context, cookie, request):
    """
    Schreibt das Cookie in die Session
    """
    session = ISession(request)
    print session
    #import pdb;pdb.set_trace()
    session['sb'] = cookie
    session.save()


def calculateStep(context, valuedata, data, basis, sbmin, sbmax, request):
    """
    Der Betreuungsaufwand der Aufgabe wird berechnet
    """
    if not valuedata:
        return 0.0
    cookie, personalaufwand = getSessionCookie(context, request)
    faktor = float(personalaufwand) * float(basis)
    stepvalue = 0.0
    for i in valuedata:
        stepvalue += faktor * float(data.get(i))
    if sbmin:
        if stepvalue < float(sbmin):
            stepvalue = float(sbmin)
    if sbmax:
        if stepvalue > float(sbmax):
            stepvalue = float(sbmax)
    return stepvalue


def delSbFromSession(context, request):
    """
    Loescht die Daten der BS-Betreuung aus dem Session-Cookie
    """
    sb_default = {'sbsum':0.0, 'sbvalues':[], 'steps':[], 'stepdata':{}}
    setSessionCookie(context, sb_default, request)


def saveStepData(context, stepnr, valuedata, commentdata, data, stepvalue, alt, request):
    """
    Schreibt die Daten des Steps in die Session
    """
    print stepnr
    print valuedata
    print stepvalue
    cookie, mitarbeiter = getSessionCookie(context, request)
    if stepnr in cookie['steps']:
        cookie['sbsum'] = cookie['sbsum'] - cookie['stepdata'][stepnr]['stepvalue']
        cookie['steps'].pop(cookie['steps'].index(stepnr))
    cookie['sbsum'] = cookie['sbsum'] + stepvalue
    cookie['sbvalues'] = list(set(cookie['sbvalues'] + valuedata))
    cookie['steps'].append(stepnr)
    cookie['stepdata'][stepnr] = {'data':data,
                                  'valuedata':valuedata,
                                  'commentdata': commentdata,
                                  'stepvalue': stepvalue,
                                  'alt':alt}
    setSessionCookie(context, cookie, request)
    return cookie


def checkStepData(context, stepnr, request):
    """
    Loescht die Daten des aktuellen Steps aus dem Cookie im Falle von Steuerung Zurueck
    """
    cookie, mitarbeiter = getSessionCookie(context, request)
    if stepnr in cookie['steps']:
        cookie['steps'].pop(cookie['steps'].index(stepnr))
        cookie['sbsum'] = cookie['sbsum'] - cookie['stepdata'][stepnr]['stepvalue']
        del cookie['stepdata'][stepnr]
    setSessionCookie(context, cookie, request)
    return cookie

