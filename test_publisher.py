#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.queue_declare(queue="hello")

while 1:

    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=str(time.gmtime())
                      )
    time.sleep(5)
    print "Sent message!"
