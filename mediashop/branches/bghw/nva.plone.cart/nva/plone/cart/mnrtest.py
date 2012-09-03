from suds.client import Client
from suds.sudsobject import asdict

def mnrtest(mnr):
    print "Test der Validierung von Mitgliedsnummern"
    sc = Client('https://bghwwebservices.bg-kooperation.de/services/Service757/Service757.asmx?WSDL')
    result = sc.service.S757(mnr,'00')
    print result
    if not result:
        return True
    if result.INFO.RETURNCODE == -1:
        if result.RESPONSE.VORHANDEN == "1":
            return True
    return False

if __name__ == "__main__":
    print mnrtest('000000025')
