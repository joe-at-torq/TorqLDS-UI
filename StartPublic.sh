#!/bin/bash

#Start Public LDS GUI

export FLASK_APP=/home/lds/WebGUI/Public/reg-form/reg-process.py
export FLASK_RUN_PORT=5000

flask run --host=0.0.0.0
