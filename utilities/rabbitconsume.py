#! /usr/local/bin/python3

import pika
import json
import os

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
cfg_RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
cfg_RABBITMQ_EXCH = "/"
cfg_RABBITMQ_QNAME =  "hello"
cfg_MESSAGES_TO_READ = 10

# Main stuff
print ("Startup")

# Start Response
channel = connect_rabbitmq(cfg_RABBITMQ_HOST,cfg_RABBITMQ_PORT,cfg_RABBITMQ_USERNAME,cfg_RABBITMQ_PASSWORD,cfg_RABBITMQ_EXCH,cfg_RABBITMQ_QNAME)
print("Connected to RabbitMQ Channel {}".format(channel), flush=True)

total = 0
resp = "ff"

# Consume a message (loop)
jsonresp = json.loads("{}")

messages = []

for i in range(cfg_MESSAGES_TO_READ):
    method_frame, header_frame, body = channel.basic_get(cfg_RABBITMQ_QNAME)
    if method_frame:
        data = json.loads(body)
        messages.append(data)
        #print(header_frame.message_id)
        #jsonresp[header_frame.message_id]=data
        #print (data)
        channel.basic_ack(method_frame.delivery_tag)
        total+=1
    else:
        print('No message returned')
        break

jsonresp["messages"] = messages
# message_string = ""
# for message in message_bodies:
#     message_string += str(message)
#     total += 1
#     # Add JSON ","
#     print ("tot {} Count {}".format(total,message_bodies.count))
#     if (total !=message_bodies.count):
#         message_string += ","

# jsonresponse = message_string    
print(json.dumps(jsonresp))
#print(json.dumps('{"error"}'))
