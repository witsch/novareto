# -*- coding: utf-8 -*-

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


def getSessionCookie(context):
    """
    Liest das SessionCookie
    """
    session = context.session_data_manager.getSessionData()
    sb_default = {'sbsum':0.0, 'sbvalues':[], 'steps':[], 'stepdata':{}}
    cookie = session.get('sb', sb_default)
    data_startseite = session.get('start', {})
    mitarbeiter = data_startseite.get('mitarbeiter', 0.0)
    if isinstance(mitarbeiter, str) or isinstance(mitarbeiter, unicode):
        mitarbeiter = float(str(mitarbeiter).replace(',','.'))
    return (cookie, mitarbeiter)


def setSessionCookie(context, cookie):
    """
    Schreibt das Cookie in die Session
    """
    session = context.session_data_manager.getSessionData()
    session.set('sb', cookie)


def calculateStep(context, valuedata, data, basis, min, max):
    """
    Der Betreuungsaufwand der Aufgabe wird berechnet
    """
    cookie, personalaufwand = getSessionCookie(context)
    print cookie, personalaufwand
    faktor = float(personalaufwand) * float(basis)
    for i in valuedata:
        faktor = faktor * float(data.get(i))
    stepvalue = faktor
    if min:
        if stepvalue < float(min):
            stepvalue = float(min)
    if max:
        if stepvalue > float(max):
            stepvalue = float(max)
    return stepvalue


def delSbFromSession(context):
    """
    Loescht die Daten der BS-Betreuung aus dem Session-Cookie
    """
    sb_default = {'sbsum':0.0, 'sbvalues':[], 'steps':[], 'stepdata':{}}
    setSessionCookie(context, sb_default)


def saveStepData(context, stepnr, valuedata, commentdata, data, stepvalue, alt):
    """
    Schreibt die Daten des Steps in die Session
    """
    cookie, mitarbeiter = getSessionCookie(context)
    cookie['sbsum'] = cookie['sbsum'] + stepvalue
    cookie['sbvalues'] = list(set(cookie['sbvalues'] + valuedata))
    cookie['steps'].append(stepnr)
    cookie['stepdata'][stepnr] = {'data':data,
                                  'valuedata':valuedata,
                                  'commentdata': commentdata,
                                  'stepvalue': stepvalue,
                                  'alt':alt}
    setSessionCookie(context, cookie)
    return cookie


def eraseStepData(context, stepnr):
    """
    Loescht die Daten des aktuellen Steps aus dem Cookie im Falle von Steuerung Zurueck
    """
    cookie, mitarbeiter = getSessionCookie(context)
    if stepnr in cookie['steps']:
        cookie['steps'].pop(cookie['steps'].index(stepnr))
        cookie['sbsum'] = cookie['sbsum'] - cookie['stepdata'][stepnr]['stepvalue']
        del cookie['stepdata'][stepnr]
    setSessionCookie(context, cookie)
    return cookie

