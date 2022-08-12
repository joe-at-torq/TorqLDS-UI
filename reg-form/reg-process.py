#!/usr/bin/python3
import time, subprocess, os
from flask import Flask, request, render_template, requests
app = Flask(__name__)

@app.route('/', methods=["GET"]) #Front page load
def form():
        return render_template('reg-form.html')

@app.route('/processform', methods=["POST"]) #On submit -> Process data
def processform():
        if request.method == 'POST':
                name = request.form.get('name')
                email = request.form['email']
                selectedclass = request.form['selectedclass']
                user_ip = request.environ['REMOTE_ADDR']
                lab_duration = request.form['labduration']

                #Adjust Parameters
                firstname,lastname=name.split(" ")
                username=firstname[0]+lastname

                #Time Stamp
                localtime = time.asctime( time.localtime(time.time()) )

                #Write Log Entry
                f = open("lds.log","a")
                f.write("#######################################\n")
                f.write("Name: "+name+"\n")
                f.write("Username: "+username+"\n")
                f.write("Email: "+email+"\n")
                f.write("Selected Class: "+selectedclass+"\n")
                f.write("Lab Duration: "+lab_duration+"\n")
                f.write("Source IP: "+user_ip+"\n")
                f.write("Request Time: "+str(localtime)+"\n")

                type = "lab"
                deployment_uui = 
                deployment_owner = 
                time = str(localtime)

                #Notify Torq For New Deployment Request
                url = f"https://cloud.tenable.com/vulns/export"
                payload = {"deployment_uuid": deployment_uui ,"deployment_owner": deployment_owner, "user_name":name, "user_email":email, "class":selectedclass, "duration":lab_duration, "user_ip":user_ip, "request_time": time}
                out = requests.post(url, headers={},json=json.dumps(payload))

                f.write("#######################################\n")
                f.close()

        return render_template('reg-summary.html') #after processing data, present the summary page