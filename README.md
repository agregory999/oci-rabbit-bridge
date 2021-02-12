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

![Architecture](OCI-Rabbit.svg)
