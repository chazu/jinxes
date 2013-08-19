from time import sleep
import uuid
import pika

class RemoteEventDispatch:
    """
    Receives messages from the rabbit server
    and passes them to the app
    """

    def register_exclusive_queue(self):
        self.channel.basic_publish(exchange='',
                                   routing_key='register_player',
                                   properties=pika.BasicProperties(
                reply_to=self.exclusive_queue_id,
                ),
                                   body="json goes here")


    def initialize_exclusive_queue(self):
        self.default_queue = self.channel.queue_declare(exclusive=True)
        self.exclusive_queue_id=self.default_queue.method.queue
        self.register_exclusive_queue()

    def __init__(self, app):

        self.connection = connection = pika.BlockingConnection()
        self.channel = channel = connection.channel()
        self.app = app
        self.initialize_exclusive_queue()

    def dispatch_message(self, channel, frame, method, body):
        print "dispatching message========================="
        print frame
        print method
        print body
        self.app.remote_messages.append(body)

    def init_consume(self):
        self.channel.basic_consume(self.dispatch_message, self.exclusive_queue_id, no_ack=True)

    def check_queue(self):
        return self.channel.consume(self.exclusive_queue_id)

