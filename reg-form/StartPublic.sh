#!/bin/bash

#Start Public LDS GUI

export FLASK_APP=${PWD}/reg-process.py
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=0

flask run --host=0.0.0.0
