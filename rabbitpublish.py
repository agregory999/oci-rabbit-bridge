#! /usr/local/bin/python3

import pika
import uuid
from datetime import date

def connect_rabbitmq(hostname,port,username,password,exchange,qname):

    try:
        credentials = pika.PlainCredentials(username,password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(hostname,port,exchange,credentials))
        print(connection)
        channel = connection.channel()
        channel.queue_declare(queue=qname)
        return channel
    except Exception as ex:
        print("Error: RabbitMQ connection failed", ex, flush=True)
        raise

cfg_RABBITMQ_HOST = "rabbitprod-integration.ociblue.agregory.page"
cfg_RABBITMQ_PORT = 5672
cfg_RABBITMQ_USERNAME = "kbk8j7E0QllYJqwFzU46oGNwPrOIstUE"
cfg_RABBITMQ_PASSWORD = "kcrzRW7bwf-33OIMATflbGv7iFXDpv6R"
cfg_RABBITMQ_EXCH = "/"
cfg_RABBITMQ_QNAME =  "hello"
# Main stuff
print ("Startup")

channel = connect_rabbitmq(cfg_RABBITMQ_HOST,cfg_RABBITMQ_PORT,cfg_RABBITMQ_USERNAME,cfg_RABBITMQ_PASSWORD,cfg_RABBITMQ_EXCH,cfg_RABBITMQ_QNAME)
print("Connected to RabbitMQ Channel {}".format(channel), flush=True)

messagebody = '{"text":"rabbit message"}'
props=pika.BasicProperties(message_id=str(uuid.uuid4()),content_type='application/json')
# Publish message
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=messagebody,
                      properties=props)
print(" [x] Sent {}".format(messagebody))
