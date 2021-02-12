import io
import json
import oci
import pika
import hashlib
import base64

from fdk import response
from base64 import b64encode, b64decode

# Main handler

def handler(ctx, data: io.BytesIO = None):
    try:
        signer = oci.auth.signers.get_resource_principals_signer()

        resp = "0-Begin" 
    
        # Construct JSON Response - add to it later
        jsonresponse = json.loads('{}')
        jsonrequest = json.loads(data.getvalue())

        try:
            cfg = ctx.Config()
            cfg_RABBITMQ_USERNAME = cfg["RABBITMQ_USERNAME"]
            cfg_RABBITMQ_PASSWORD_OCID = cfg["RABBITMQ_PASSWORD_OCID"]
            cfg_RABBITMQ_HOST = cfg["RABBITMQ_HOST"]
            cfg_RABBITMQ_PORT = cfg["RABBITMQ_PORT"]
            cfg_RABBITMQ_EXCH = cfg["RABBITMQ_EXCH"]
            cfg_RABBITMQ_QNAME = cfg["RABBITMQ_QNAME"]
            cfg_MESSAGES_TO_READ = jsonrequest.get("messages")
            resp += "0-MessagesToRead:{}".format(cfg_MESSAGES_TO_READ)
        except Exception as ex:
            resp += "|0-Incorrect Config - Specify messages"
            jsonresponse["ReturnCodes"] = resp
            return response.Response(
                ctx,
                response_data=jsonresponse,
                headers={"Content-Type": "application/json"}
            )

        # Construct JSON Response - add to it later
        jsonresponse = json.loads('{}')
        jsonrequest = json.loads(data.getvalue())

        # Get Password
        try:
            password = get_text_secret(cfg_RABBITMQ_PASSWORD_OCID)
            print("Password: {}".format(password))
        except Exception as ex:
            resp += "|0-Incorrect Config - Password not avail"
            jsonresponse["ReturnCodes"] = resp
            return response.Response(
                ctx,
                response_data=jsonresponse,
                headers={"Content-Type": "application/json"}
            )

        # Connect RabbitMQ
        try:
            channel = connect_rabbitmq(cfg_RABBITMQ_HOST,cfg_RABBITMQ_PORT,cfg_RABBITMQ_USERNAME,password,cfg_RABBITMQ_EXCH,cfg_RABBITMQ_QNAME)
            print("Connected to RabbitMQ Channel {}".format(channel), flush=True)
            resp += "|1-RMQConnect {} {}".format(cfg_RABBITMQ_HOST,cfg_RABBITMQ_PORT)
        except Exception as ex:
            resp += "|1x-RMQFail {}".format(ex)

        # While loop - Grab a message from the channel (maybe wrap this in a loop until Q is drained)
        totalprocessed = 0
        #message_bodies = ""
        for i in range(cfg_MESSAGES_TO_READ):
            # Read a single message
            method_frame, header_frame, body = channel.basic_get(cfg_RABBITMQ_QNAME)
            if method_frame:
                print(method_frame, header_frame, body)
                channel.basic_ack(method_frame.delivery_tag)
                print("Message ID: {}".format(header_frame.message_id),flush=True)
                resp += "|4-MessageRead {}".format(header_frame.message_id)
                jsonresponse[header_frame.message_id]=str(body)
                #message_bodies += str(body)
                totalprocessed += 1

            else:
                break
        # Completed loop
        resp += "|5-MessageCount {}".format(totalprocessed)

        #Add in original request and Control Data
        jsonresponse["ReturnCodes"] = resp
        jsonresponse["OriginalRequest"] = jsonrequest

        return response.Response(
            ctx,
            response_data=jsonresponse,
            headers={"Content-Type": "application/json"}
        )
    except Exception as ex:
        return response.Response(
            ctx,
            response_data='{"error"}',
            headers={"Content-Type": "application/json"}
        )
################################## Support Functions ###############################################    
# Get Secret from OCID
def get_text_secret(secret_ocid):
    #decrypted_secret_content = ""
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        client = oci.secrets.SecretsClient({}, signer=signer)
        secret_content = client.get_secret_bundle(secret_ocid).data.secret_bundle_content.content.encode('utf-8')
        decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    except Exception as ex:
        print("ERROR: failed to retrieve the secret content", ex, flush=True)
        raise
    return decrypted_secret_content

# RabbitMQ Access
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
