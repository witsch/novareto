from uvc.api import api
from bgetem.praevention.doku_praevention import IDokuPraevention

api.templatedir('templates')

class PraevDocView(api.Page):
    api.context(IDokuPraevention)
