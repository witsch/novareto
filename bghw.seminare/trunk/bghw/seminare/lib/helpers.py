# -*- coding: utf-8 -*-

def formatDate(datetime):
    date = datetime
    if datetime:
        date = "%s.%s.%s" %(datetime[8:10], datetime[5:7], datetime[0:4])
    return date    


def mapper(myform):
    """
    mappt die Daten der Form auf das aktuelle PDF
    """
    uebernachtung = ''
    if myform.get('nacht', 'False') == 'True':
        if myform.get('reservierung-von-uebernachtungsmoeglichkeiten', 'nein') == 'ja':
            uebernachtung = 'j'
        else:
            uebernachtung = 'n'

    daten = {'Datum' : myform.get('modification', ''),
             'Seminartyp' : '',
             'S1_Kommtaus': myform.get('funktion-im-betrieb', ''),
             'S1_Kommtaus1': myform.get('sonstige-funktion-im-betrieb', ''),
             'S1_Vorname': myform.get('vorname', ''),
             'S1_Nachname': "%s %s %s" %(myform.get('anrede', ''), myform.get('akad_titel', ''), myform.get('name', '')),
             'S1_Geburtsdatum': formatDate(myform.get('geburtsdatum', '')),
             'S1_SEM_Uebernachtung' : uebernachtung,
             'S1_MitarbeiterVon': myform.get('datum-der-einstellung', ''),
             'S1_Firma':  myform.get('name-der-firma-betriebsstaette', ''),
             'S1_MGLNR': myform.get('mitgliedsnummer', ''),
             'S1_Strasse': myform.get('strasse-und-hausnummer', ''),
             'S1_PLZ': myform.get('postleitzahl', ''),
             'S1_Ort': myform.get('ort', ''),
             'S1_Telefon': myform.get('telefon', ''),
             'S1_EMail': myform.get('replyto', ''),
             'S1_Sparte': '',
             'S1_SEM_Zeichen': myform.get('stype', ''),
             'S1_SEM_Ort': myform.get('sort', ''),
             'S1_SEM_von': myform.get('von', '')[:10],
             'S1_SEM_bis': myform.get('bis', '')[:10],
             'S1_SEM_folgetermin': '',
             'S1_SEM_folge_von': '',
             'S1_SEM_folge_bis': '',
             'S1_SEM_buchungsinfo': myform.get('ausgebucht', ''),
             'S1_AP_Vorname': myform.get('vorname-der-ansprechperson', ''),
             'S1_AP_Nachname': myform.get('nachname-der-ansprechperson', ''),
             'S1_AP_Strasse': myform.get('strasse-und-hausnummer-der-ansprechperson', ''),
             'S1_AP_Ort': myform.get('postleitzahl-und-ort-der-ansprechperson', ''),
             'S1_AP_Telefax': myform.get('telefon-der-ansprechperson', ''),
             'S1_AP_EMail': myform.get('e-mail-adresse-der-ansprechperson', ''),
             'S1_SEM_Veranstalter': '',
             'S2_Vorname': myform.get('vorname', ''),
             'S2_Nachname': "%s %s %s" %(myform.get('anrede', ''), myform.get('akad_titel', ''), myform.get('name', '')),
             'S2_Geburtsdatum': formatDate(myform.get('geburtsdatum', '')),
             'S2_Geburtsort': '',
             'S2_Strasse': myform.get('privater-wohnort-strasse-und-hausnummer', ''),
             'S2_PLZ': myform.get('privater-wohnort-postleitzahl', ''),
             'S2_Ort': myform.get('privater-wohnort-ort', ''),
             'S2_anzahl_mitarbeiter': myform.get('anzahl-mitarbeiter', ''),
             'S2_voraussetzungen_mitarbeiter_taetig': myform.get('50-arbeitsstunden-jahr', ''),
             'S2_tab_besprochen': myform.get('besprechung-mit-tab', ''),
             'S2_jahre_taetig1': myform.get('arbeitsjahre', ''),
             'S2_jahre_taetig2': myform.get('arbeitsjahre', ''),
             'S2_taetig_als': myform.get('beschreibung-der-funktion-im-betrieb', ''),
             'S2_ausbildung': myform.get('branchenspezifische-ausbildung-praesenzphase-pv', ''),
             'S2_betriebsrat': myform.get('betriebsrat', ''),
             'S2_job': myform.get('berufliche-voraussetzungen', ''),
              }
    return daten

