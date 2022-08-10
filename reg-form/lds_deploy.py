#!/usr/bin/python

import sys, subprocess, os

#python lds_deploy.py test JDillig +18172695082 comptech.joe@gmail.com 2

#Input Variables
user_lab=sys.argv[1]
user_name=sys.argv[2]
user_phone=sys.argv[3]
user_email=sys.argv[4]
user_lab_duration=sys.argv[5]

#Send Creation Notifications
subprocess.call('python lds_nofity.py '+user_phone+' Deployment underway for the '+user_lab+' environment. You will recieve login information once the deployment is complete.', cwd=user_working_dir+'/'+user_name, shell=True)

#Create User Directory
user_working_dir=os.getcwd()+'/environments/'+user_lab
subprocess.call('mkdir '+user_working_dir+'/'+user_name , shell=True)
subprocess.call('cp '+user_working_dir+'/main.tf '+user_working_dir+'/'+user_name+'/main.tf' , shell=True)

#Terraform init
subprocess.call('terraform init', cwd=user_working_dir+'/'+user_name, shell=True)

#Terraform Create Apply Plan
subprocess.call('terraform plan -out='+str(user_name)+'_Apply_Plan -var "USERNAME='+user_name+'" -var "ENVIRONMENT='+user_lab+'"', cwd=user_working_dir+'/'+user_name, shell=True)

#Terraform Apply Plan
subprocess.call('terraform apply '+str(user_name)+'_Apply_Plan', cwd=user_working_dir+'/'+user_name, shell=True)

#Terraform Create Destroy Plan 
subprocess.call('terraform plan -destroy -out='+str(user_name)+'_Destroy_Plan -var "USERNAME='+user_name+'" -var "ENVIRONMENT='+user_lab+'"', cwd=user_working_dir+'/'+user_name, shell=True)

#Call LDS Scheduler
subprocess.Popen('python lds_schedule.py '+str(user_lab)+' '+str(user_name)+' '+str(user_phone)+' '+str(user_email)+' '+str(user_lab_duration)+' &', cwd=os.getcwd(), shell=True)