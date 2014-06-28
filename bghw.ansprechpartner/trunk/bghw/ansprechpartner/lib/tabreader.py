# -*- coding: utf-8 -*-
# author: lwalther@novareto.de
from xlrd import open_workbook

regdirs = {u'Bremen':{'tel':'0421 30170 0','mail':'bremen@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-bremen'},
           u'Hamburg':{'tel':'040 30613 0', 'mail':'hamburg@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-hamburg'},
           u'Berlin':{'tel':'030 85301 0', 'mail':'berlin@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-berlin'},
           u'Gera': {'tel':'0365 77330 0', 'mail':'gera@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-gera'},
           u'München': {'tel':'', 'mail':'', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-muenchen'},
           u'Mannheim': {'tel':'0621 183 0', 'mail':'mannheim@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-mannheim'},
           u'Mainz': {'tel':'06131 4993 0', 'mail':'mainz@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-mannheim'},
           u'Bonn': {'tel':'0228 5406 0', 'mail':'bonn@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-bonn'},
           u'Essen': {'tel':'0201 12506 0', 'mail':'essen@bghw.de', 'url':'http://www.bghw.de/wir-ueber-uns/adressen/standort-essen'},
          }

def findTabByPlz(plz, data):
    wb = open_workbook(file_contents = data)
    sheet = wb.sheet_by_name('Postleitzahlen')
    cols = sheet.ncols
    for row in range(sheet.nrows):
        if sheet.cell(row, 0).value == plz:
            data = {}
            data['plz'] = sheet.cell(row,0).value
            data['ort'] = sheet.cell(row,1).value
            data['tab'] = sheet.cell(row,4).value
            data['tab-tel'] = sheet.cell(row,5).value
            data['tab-mail'] = sheet.cell(row,6).value
            data['rd'] = '%s / %s' %(sheet.cell(row,2).value, sheet.cell(row,3).value)
            mykey = sheet.cell(row,3).value
            data['rd-url'] = regdirs[mykey.strip()]['url']
            data['rd-tel'] = regdirs[mykey.strip()]['tel']
            data['rd-mail'] = regdirs[mykey.strip()]['mail']
            data['pb'] = sheet.cell(row,7).value
            data['pb-tel'] = sheet.cell(row,8).value
            data['pb-mail'] = sheet.cell(row,9).value
            return data

def findTabByOrt(ort, data):
    values = []
    wb = open_workbook(file_contents = data)
    sheet = wb.sheet_by_name('Postleitzahlen')
    cols = sheet.ncols
    for row in range(sheet.nrows):
        if sheet.cell(row, 1).value.startswith(ort):
            data = {}
            data['plz'] = sheet.cell(row,0).value
            data['ort'] = sheet.cell(row,1).value
            data['tab'] = sheet.cell(row,4).value
            data['tab-tel'] = sheet.cell(row,5).value
            data['tab-mail'] = sheet.cell(row,6).value
            data['rd'] =  '%s / %s' %(sheet.cell(row,2).value, sheet.cell(row,3).value)
            mykey = sheet.cell(row,3).value
            data['rd-url'] = regdirs[mykey.strip()]['url']
            data['rd-tel'] = regdirs[mykey.strip()]['tel']
            data['rd-mail'] = regdirs[mykey.strip()]['mail']
            data['pb'] = sheet.cell(row,7).value
            data['pb-tel'] = sheet.cell(row,8).value
            data['pb-mail'] = sheet.cell(row,9).value
            values.append(data)
    return values

def findAdrByNr(nr, sheet):
    addr = {}
    for row in range(sheet.nrows):
        if nr == sheet.cell(row,0).value:
            addr['rd'] = sheet.cell(row,2).value
            addr['strnr'] = sheet.cell(row,3).value
            addr['plz'] = str(sheet.cell(row,4).value).split('.')[0]
            addr['ort'] = sheet.cell(row,5).value
            addr['tel'] = sheet.cell(row,6).value
            addr['fax'] = sheet.cell(row,7).value
    return addr        

def findRehaByPlzName(plz, name, data):
    wb = open_workbook(file_contents = data)
    sheet = wb.sheet_by_name('PLZ-Name')
    rosheet = wb.sheet_by_name('Standorte')
    for row in range(sheet.nrows):
        if row > 0:
            if int(sheet.cell(row,0).value) <= int(plz) <= int(sheet.cell(row,1).value):
                if sheet.cell(row,2).value.lower() <= name.lower() <= sheet.cell(row,3).value.lower():
                    rdadr = findAdrByNr(sheet.cell(row,4).value, rosheet)
                    rdadr['webcode'] = sheet.cell(row,5).value
                    return rdadr
