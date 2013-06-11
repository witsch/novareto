import grok

from amqptest import resource

class Amqptest(grok.Application, grok.Container):
    title = u"HALLO"

class Index(grok.View):
    def update(self):
        resource.style.need()
