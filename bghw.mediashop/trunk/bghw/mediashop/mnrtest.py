from z3c.suds import get_suds_client
from suds.sudsobject import asdict

def mnrtest(mnr):
    try:
        client = get_suds_client('https://bghwwebservices.bg-kooperation.de/services/Service757/Service757.asmx?WSDL')
    except:
        return True
    result = client.service.S757(mnr,'00')
    if not result:
        return True
    if result.INFO.RETURNCODE == -1:
        if result.RESPONSE.VORHANDEN == "1":
            return True
    return False

if __name__ == "__main__":
    print mnrtest('000000025')

