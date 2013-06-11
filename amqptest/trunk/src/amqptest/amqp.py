# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import transaction
from kombu import Connection
from amqptest.send import queue


def main(app, root):

    def doit(body, message):
        app = root['app']
        import pdb; pdb.set_trace()
        app.title = body['title']
        message.ack()
        import transaction; transaction.commit()

    with Connection('amqp://guest:guest@localhost//') as conn:
        with conn.Consumer(queue, callbacks=[doit]) as consumer:
            # Process messages and handle events on all channels
            while True:
                conn.drain_events()


if __name__ == "__main__":
    main(app, root)
