#!/usr/bin/python3
import time, subprocess, os, requests, json
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

                #Gather Instance Details
                lds_settings = open('lds_settings.json')
                data = json.load(lds_settings)

                #Notify Torq For New Deployment Request
                url = data['webhook']
                payload = {"notification_type":"new_lab_request", "deployment_uuid": data['uuid'] ,"deployment_owner": data['owner'], "user_name":name, "user_email":email, "class":selectedclass, "duration":lab_duration, "user_ip":user_ip, "request_time": str(localtime)}
                out = requests.post(url, headers={},json=json.dumps(payload))

                f.write("#######################################\n")
                lds_settings.close()
                f.close()

        return render_template('reg-summary.html') #after processing data, present the summary page