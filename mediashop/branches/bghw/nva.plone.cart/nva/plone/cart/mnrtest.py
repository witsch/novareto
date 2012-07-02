from suds.client import Client
from suds.sudsobject import asdict

def mnrtest(mnr):
    print "Test der Validierung von Mitgliedsnummern"
    sc = Client('http://10.30.0.86/services/Service757/Service757.asmx?WSDL')
    #sc.set_options(location='http://bghwwebservices.bg-kooperation.de/services/Service723/SERVICE723.asmx')
    result = sc.service.S757(mnr,'00')
    if result.INFO.RETURNCODE == -1:
        if result.RESPONSE.VORHANDEN == "1":
            return True
    return False
