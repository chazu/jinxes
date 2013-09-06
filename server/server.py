import pika


parameters = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue="rcon")

channel.basic_publish(exchange='',
                      routing_key="rcon",
                      body="Hello rcon!")
print "Sent hello rcon"
