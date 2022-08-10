#!/usr/bin/python

import sys, subprocess, os, boto3

#############################################################
# lds_notify.py (LDS Component)
# Uses AWS SES to notify students when cloud labs are built
# Joe Dillig - Checkpoint Software 6-3-19
##############################################################


#python lds_notify.py +18172695082 "Welcome to the Lab Deployment System!"

#Input Variables
user_phone=sys.argv[1]
user_message=sys.argv[2]

#Send User SMS using AWS SMS
sns = boto3.client('sns')
sns.publish(PhoneNumber=user_phone, Message=user_message)