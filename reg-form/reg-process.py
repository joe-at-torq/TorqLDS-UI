#!/usr/bin/python
import time, subprocess, os
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=["GET"]) #Front page load
def form():
	return render_template('reg-form.html')

@app.route('/processform', methods=["POST"]) #On submit -> Process data
def processform():
	if request.method == 'POST': 
		name = request.form.get('name')
		email = request.form['email']
		countrycode = request.form['countrycode']
		phone = request.form['phone']
		selectedclass = request.form['selectedclass']
		user_ip = request.environ['REMOTE_ADDR']
		lab_duration = request.form['labduration']

		#Adjust Parameters
		firstname,lastname=name.split(" ")
		username=firstname[0]+lastname
		fullphone='+'+countrycode+phone

		#Time Stamp
		localtime = time.asctime( time.localtime(time.time()) )

		#Write Log Entry
		f = open("lds.log","a")
		f.write("#######################################\n")
		f.write("Name: "+name+"\n")
		f.write("Username: "+username+"\n")
		f.write("Email: "+email+"\n")
		f.write("Phone Number: "+fullphone+"\n")
		f.write("Selected Class: "+selectedclass+"\n")
		f.write("Lab Duration: "+lab_duration+"\n")
		f.write("Source IP: "+user_ip+"\n")
		f.write("Request Time: "+str(localtime)+"\n")

		#Send data to lds_deploy.py
		#print ('python lds_deploy.py '+str(selectedclass)+' '+str(username)+' '+str(fullphone)+' '+str(email)+' '+str(lab_duration))
		subprocess.Popen('python lds_deploy.py '+str(selectedclass)+' '+str(username)+' '+str(fullphone)+' '+str(email)+' '+str(lab_duration)+' &', cwd=os.getcwd(), shell=True)
		#Example:  python lds_deploy.py Automation Training JDillig +18172695082 comptech.joe@gmail.com 2

		
		f.write("#######################################\n")
                f.close()

	return render_template('reg-summary.html') #after processing data, present the summary page
