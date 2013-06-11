# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


from kombu import Connection, Exchange, Queue

exchange = Exchange('media', 'direct', durable=True)
queue = Queue('video', exchange=exchange, routing_key='doit')


if __name__ == "__main__":

    with Connection('amqp://guest:guest@localhost//') as conn:
        with conn.Producer(serializer='json') as producer:
            producer.publish({'title': 'Christian Ist Der ALLERBISET'},
                            exchange=exchange, routing_key='doit',
                            declare=[queue])
