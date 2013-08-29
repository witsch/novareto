from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_telefon(self):
        return self.context.getProperty('telefon', '')
    def set_telefon(self, value):
        return self.context.setMemberProperties({'telefon': value})
    telefon  = property(get_telefon , set_telefon )

    def get_mobile (self):
        return self.context.getProperty('mobile', '')
    def set_mobile (self, value):
        return self.context.setMemberProperties({'mobile': value})
    mobile  = property(get_mobile , set_mobile )

