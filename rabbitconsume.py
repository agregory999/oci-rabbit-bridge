#! /usr/local/bin/python3

import pika
import json

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
cfg_MESSAGES_TO_READ = 10

# Main stuff
print ("Startup")

# Start Response
channel = connect_rabbitmq(cfg_RABBITMQ_HOST,cfg_RABBITMQ_PORT,cfg_RABBITMQ_USERNAME,cfg_RABBITMQ_PASSWORD,cfg_RABBITMQ_EXCH,cfg_RABBITMQ_QNAME)
print("Connected to RabbitMQ Channel {}".format(channel), flush=True)

total = 0
resp = "ff"

# Consume a message (loop)
jsonresp = json.loads('{}')
message_bodies = []
for i in range(cfg_MESSAGES_TO_READ):
    method_frame, header_frame, body = channel.basic_get(cfg_RABBITMQ_QNAME)
    if method_frame:
        print(method_frame, header_frame, body)
        jsonresp[header_frame.message_id]=body
        print (str(body))
        channel.basic_ack(method_frame.delivery_tag)
        total+=1
    else:
        print('No message returned')
        break

jsonresp['codes'] = '{"ret":"retv"}'
# message_string = ""
# for message in message_bodies:
#     message_string += str(message)
#     total += 1
#     # Add JSON ","
#     print ("tot {} Count {}".format(total,message_bodies.count))
#     if (total !=message_bodies.count):
#         message_string += ","

# jsonresponse = message_string    
print("Done Reading {} message".format(jsonresp))
