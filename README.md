# OCI RabbitMQ Bridge

The purpose of this example is to show that an Oracle Function can consum e messages from an external RabbitMQ environment and provide them to a caller.  In this case, the Function is exposed via Oracle API Gateway and a public endpoint, protected by OAtuh.  The caller ultimately is an Oracle Integration Cloud environment, where the message contents are required to process be brought in and transformed before going to their final destination.

Rather than running something that constantly needs attention to consume messages from RMQ, the function takes a parameter named "messages", which determines the number of messages to pull from the Queue and return.  

## Installation

This example require the following:

- A working VCN with public and private subnet
- Oracle Functions context set up
- Access via Dynamic Group and Policy for Oracle Functions to consume secrets

The basic process is to install the function into a function app, then connect it to an API Gateway that exists or can be created easily.  The function requires configuration parameters to be set in order to connect ot RabbitMQ, which must be publicly accessible.  NOTE - internally this could be accessible via VPN/FastConnect settings to on-prem or another Oracle VCN.

## Overall Architecture

![Architecture](images/OCI-Rabbit.svg)

## Utilities

Included are simple python scripts to publish a test message and to consume messages from Rabbit MQ.  To use them, export the password and edit the parameters in the script:

```bash

prompt> export RABBITMQ_PASSWORD=xxxxx
prompt> ./rabbitpublish.py
Startup
<BlockingConnection impl=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x106b13e20> params=<ConnectionParameters host=rabbitprod-integration.ociblue.agregory.page port=5672 virtual_host=/ ssl=False>>>
Connected to RabbitMQ Channel <BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x106b13e20> params=<ConnectionParameters host=rabbitprod-integration.ociblue.agregory.page port=5672 virtual_host=/ ssl=False>>>>
 [x] Sent {"text":"rabbit message"}

prompt> ./rabbitconsume.py
Startup
<BlockingConnection impl=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x107c48850> params=<ConnectionParameters host=rabbitprod-integration.ociblue.agregory.page port=5672 virtual_host=/ ssl=False>>>
Connected to RabbitMQ Channel <BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x107c48850> params=<ConnectionParameters host=rabbitprod-integration.ociblue.agregory.page port=5672 virtual_host=/ ssl=False>>>>
<Basic.GetOk(['delivery_tag=1', 'exchange=', 'message_count=0', 'redelivered=False', 'routing_key=hello'])> <BasicProperties(['content_type=application/json', 'message_id=1de0d00f-942f-45b5-a026-c9e20771a155'])> b'{"text":"rabbit message"}'
b'{"text":"rabbit message"}'
No message returned
Done Reading {'1de0d00f-942f-45b5-a026-c9e20771a155': b'{"text":"rabbit message"}', 'codes': '{"ret":"retv"}'} message

```
