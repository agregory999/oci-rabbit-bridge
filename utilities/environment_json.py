#! /usr/local/bin/python3

import io
import os
import json
import logging

try:
    response = json.dumps(os.environ['ABC'])
    #for envvar in os.environ:
    #    response[envvar] = json.loads(os.environ[envvar])
    print(response)
except Exception as ex:
    raise
