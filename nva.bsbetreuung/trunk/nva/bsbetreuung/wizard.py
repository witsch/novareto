# -*- coding: utf-8 -*-
from collective.beaker.interfaces import ISession
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    client = MongoClient('localhost', 27017)
    db = client.bsb_database
    collection = db.bsb_collection
    sb_default = {'sbsum':0.0, 'sbvalues':[], 'steps':[], 'stepdata':{}}
    mongo_objid = session.get('sb', '')
    if not mongo_objid:
        cookie = sb_default
    else:
        cookie = collection.find_one({"_id":ObjectId(mongo_objid)})
    data_startseite = session.get('start', {})
    mitarbeiter = data_startseite.get('mitarbeiter', 0.0)
    if isinstance(mitarbeiter, str) or isinstance(mitarbeiter, unicode):
        mitarbeiter = float(str(mitarbeiter).replace(',','.'))
    print 'Cookie' *9
    print cookie
    print 'Cookie' *9
    return (cookie, mitarbeiter)


def setSessionCookie(context, cookie, request):
    """
    Schreibt das Cookie in die Session
    """
    session = ISession(request)
    client = MongoClient('localhost', 27017)
    db = client.bsb_database
    collection = db.bsb_collection
    post_id = collection.save(cookie)
    session['sb'] = post_id.__str__()
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
    cookie, mitarbeiter = getSessionCookie(context, request)
    if stepnr in cookie['steps']:
        cookie['sbsum'] = cookie['sbsum'] - cookie['stepdata'][stepnr.replace('.', '_')]['stepvalue']
        cookie['steps'].pop(cookie['steps'].index(stepnr))
    #BGHW Spezifikum zur Behandlung von Aufgabengebiet 1
    if stepnr.startswith('1') and not stepnr == '1.4':
        if cookie['stepdata'].has_key('1G'):
            oldvalue = cookie['stepdata']['1G']['stepvalue']
            cookie['sbsum'] = cookie['sbsum'] - oldvalue
        else:
            cookie['steps'].append('1G')
        cookie['stepdata']['1G'] = {'data':data,
                                    'valuedata':valuedata,
                                    'commentdata':commentdata,
                                    'stepvalue':stepvalue}
    #Ende
    cookie['sbsum'] = cookie['sbsum'] + stepvalue
    cookie['sbvalues'] = list(set(cookie['sbvalues'] + valuedata))
    cookie['steps'].append(stepnr)
    cookie['stepdata'][stepnr.replace('.', '_')] = {'data':data,
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
        cookie['sbsum'] = cookie['sbsum'] - cookie['stepdata'][stepnr.replace('.','_')]['stepvalue']
        del cookie['stepdata'][stepnr.replace('.', '_')]
    setSessionCookie(context, cookie, request)
    return cookie

