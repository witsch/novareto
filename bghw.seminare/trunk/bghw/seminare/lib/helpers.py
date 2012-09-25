# -*- coding: utf-8 -*-

def mapper(myform):
    """
    mappt die Daten der Form auf das aktuelle PDF
    """
    uebernachtung = ''
    if myform.get('nacht', 'False') == 'True':
        if myform.get('uebernachtung-reservieren', 'False') == 'True':
            uebernachtung = 'j'
        else:
            uebernachtung = 'n'

    daten = {'Datum' : myform.get('modification', ''),
             'Seminartyp' : '',
             'S1_Kommtaus': myform.get('funktion-im-betrieb', ''),
             'S1_Kommtaus1': myform.get('sonstige-funktion-im-betrieb', ''),
             'S1_Vorname': "%s %s %s" %(myform.get('anrede', ''), myform.get('akad_titel', ''), myform.get('vorname', '')),
             'S1_Nachname': myform.get('name', ''),
             'S1_Geburtsdatum': myform.get('geburtsdatum', ''),
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
             'S2_Nachname': myform.get('name', ''),
             'S2_Geburtsdatum': myform.get('geburtsdatum', ''),
             'S2_Geburtsort': '',
             'S2_Strasse': '',
             'S2_PLZ': '',
             'S2_anzahl_mitarbeiter': '',
             'S2_voraussetzungen_mitarbeiter_taetig': '',
             'S2_tab_besprochen': '',
             'S2_jahre_taetig1': '',
             'S2_jahre_taetig2': '',
             'S2_taetig_als': '',
             'S2_sparte': '',
             'S2_betriebsrat': '',
             'S2_job': '',
             'S2_teilgenommen': '',
             'S2_sidienst': '',
              }
    return daten

