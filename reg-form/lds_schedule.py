#!/usr/bin/python

import sys, subprocess, os

#python lds_schedule.py AutomationTraining JDillig +18172695082 comptech.joe@gmail.com 2

#Input Variables
user_lab=sys.argv[1]
user_name=sys.argv[2]
user_phone=sys.argv[3]
user_email=sys.argv[4]
user_lab_duration=sys.argv[5]

#LDS Schedule
# Use to schedule the deletion of an environment
# Uses the Linux "at" utility

#Write Cleanup Script
f = open("environments/"+user_lab+"/"+user_name+"/Cleanup.sh", "w")
f.writelines(["#!/bin/bash\n", "cd /home/dev/LDS/Public/reg-form/environments/"+user_lab+"/"+user_name+";terraform apply "+user_name+"_Destroy_Plan\n"])
f.close()

#Schedule Delete Notifications

#30 Min Warning
user_delete_warning_time=((60*int(user_lab_duration)) - 30)

subprocess.call("echo 'python /home/dev/LDS/Public/reg-form/lds_notify.py '"+user_phone+"' Notice: The '"+user_lab+"' environment will expire in 30 minutes!' | at now + "+str(user_delete_warning_time)+" minutes", shell=True)

#Schedule Auto Delete
subprocess.call("at now + "+user_lab_duration+" hours -f /home/dev/LDS/Public/reg-form/environments/"+user_lab+"/"+user_name+"/Cleanup.sh" , shell=True)