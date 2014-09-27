from cromlech.browser.testing import TestRequest
from grokcore.component import Context
from zope.component import getMultiAdapter
from infrae.testbrowser import Browser


class TestClass:
    request = TestRequest()
    context = Context()

    def test_example(self):
        assert 1 == 1

    def test_view(self, config, root):
        view = getMultiAdapter((root, self.request), name='index')
        view.update()
        assert "Hersteller" in view.render()

    def test_browser(self, app):
        browser = Browser(app)
        browser.open('http://localhost/addhersteller')
        form = browser.get_form(id="form")

        def addValue(field, value):
            control = form.get_control(field)
            control.value = value
            return control

        addValue("form.field.name", "Novareto")
        addValue("form.field.title", "Novareto")
        addValue("form.field.anschrift1", "Novareto")
        addValue("form.field.land", "Deutschland")
        addValue("form.field.telefon", "0911/7807238")
        addValue("form.field.homepage", "http://www.novareto.de")
        status = form.submit("form.action.uvcsite.add")

        browser.open('http://localhost/')
        assert status == 200
        assert '<a href="Novareto">Novareto</a>' in browser.contents
