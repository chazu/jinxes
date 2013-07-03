from time import sleep
import pika

class RemoteEventDispatch:
    """
    Receives messages from the rabbit server
    and passes them to the app
    """

    def __init__(self, queue, app):

        self.connection = connection = pika.BlockingConnection()
        self.channel = channel = connection.channel()
        self.queue_name = queue
        self.queue = self.channel.queue_declare(queue=self.queue_name)
        self.app = app

    def dispatch_message(self, message):
        self.app.remote_messages.append(message)

    def init_consume(self):
        self.channel.basic_consume(self.dispatch_message, self.queue_name, no_ack=True)

    def check_queue(self):
        self.channel.consume(self.queue_name)
