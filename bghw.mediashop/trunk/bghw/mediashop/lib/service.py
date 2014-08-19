# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de
from suds.client import Client
import logging
logging.basicConfig(level=logging.INFO)

URL = "http://10.30.4.22/services/service763/service763.asmx?wsdl"

client = Client(URL)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)

def addToWS(data):
   factory_order = client.factory.create('objSERVICE763')
   factory_listOfArtikel = client.factory.create('ArrayOfObj763Artikel')
   rc = []
   print data.get('bestellung')
   for artikel in data.get('bestellung'):
       factory_artikel = client.factory.create('obj763Artikel')
       factory_artikel.ARTIKELNUMMER = artikel.artikel
       factory_artikel.MENGE = artikel.anzahl
       factory_artikel.EINZELPREIS = 0 
       factory_artikel.PREIS = 0
       rc.append(factory_artikel)
   factory_listOfArtikel.obj763Artikel = rc

   factory_order.MITGLNR = data.get('mitgliedsnummer'),
   factory_order.FIRMA = data.get('firma'),
   factory_order.VORNAMENAME = u"%s %s %s %s" % (data.get('anrede'), 
                                                 data.get('titel'),
                                                 data.get('vorname'),
                                                 data.get('name'))
   factory_order.STRASSE = data.get('strhnr'),
   factory_order.PLZ = data.get('plz'),
   factory_order.ORT = data.get('ort'),
   factory_order.TELEFON = data.get('telefon'),
   factory_order.TELEFAX = "",
   factory_order.EMAIL = data.get('email'),
   factory_order.LAND = "D",
   factory_order.USTID = "",
   factory_order.ALFIRMA = data.get('a_firma'),
   factory_order.ALVORNAMENAME = u"%s %s %s %s" % (data.get('a_anrede'),
                                                   data.get('a_titel'),
                                                   data.get('a_vorname'),
                                                   data.get('a_name'))
   factory_order.ALSTRASSE = data.get('a_strhnr'),
   factory_order.ALPLZ = data.get('a_plz'),
   factory_order.ALORT = data.get('a_ort'),
   factory_order.LSTARTIKEL = factory_listOfArtikel,

   print factory_order

   ret = client.service.S763(factory_order)
   print ret

   if ret:
       print ret
       if ret.INFO.RETURNCODE == -1:
           print ret.RESPONSE.BESTELLNUMMER
           return ret.RESPONSE.BESTELLNUMMER

   return None

