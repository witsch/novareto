from xlrd import open_workbook
from App.config import getConfiguration

config = getConfiguration()
configuration = config.product_config.get('seminare', dict())
xlsfile = configuration.get('xlsfile')
wb = open_workbook(xlsfile)
so = wb.sheet_by_name('seminarorte')

def locations(key = None):
    data = {}
    if not key:
        for row in range(so.nrows):
            if row > 0:
                data[int(so.cell(row, 1).value)] = so.cell(row, 0).value
    return data
