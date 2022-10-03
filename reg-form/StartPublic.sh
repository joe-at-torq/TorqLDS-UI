#!/bin/bash

#Start Public LDS GUI

export FLASK_APP=${PWD}/reg-process.py
export FLASK_RUN_PORT=443
export FLASK_DEBUG=0

flask run --host=0.0.0.0 --cert=cert.pem --key=key.pem
