""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

from flask import Flask, request, Response
import requests

app = Flask(__name__)

#Global variables
#TODO Set corresponding values
switch_sensor_token = "[Add here token for Webhook - Switch online/offline sensor]"
power_sensor_token = "[Add here Webhook - Switch Power supply up/down sensor]"
meraki_webhook_secret = "[Add here webhook secret]"
port = "[Add here sensor port]"

#Further global variables
headers = {"Content-Type": "application/xml"}
base_url = "http://127.0.0.1:" + port

#Execute POST request with given endpoint url and payload
def post(payload, token):
    global base_url, headers
    request_url = "{}/{}".format(base_url, token)
    print(request_url)
    response = requests.post(request_url, headers=headers, data = payload)
    if response.status_code != 200:
        print('An error happend: Code:')
        print(response.status_code)    
    return response.json()

#Routes
@app.route('/webhook', methods=['POST'])
def respond():

    global switch_sensor_token, power_sensor_token, meraki_webhook_secret, port

    print("Meraki Webhook-Alert:")
    print(request.json)

    #Check if Meraki Webhook Secret is as expected
    if (request.json['sharedSecret'] == meraki_webhook_secret):
        
        #Define payload for PRTG webhook based on the received Meraki webhook alert level and content
        alertLevel = request.json['alertLevel']

        if (alertLevel == "critical"):
            payload = "<prtg><error>1</error><text>"+ request.json['alertType'] +"(Device:"+ request.json['deviceMac'] +")</text></prtg>"
        elif(alertLevel == "warning"):
            payload = "<prtg><result><channel>Alert Level</channel><value>1</value><ValueLookup>prtg.customlookups.singleint.alert</ValueLookup></result><text>"+ request.json['alertType'] +" (Device:"+ request.json['deviceMac'] +")</text></prtg>"
        elif(alertLevel == "informational"):
            payload = "<prtg><result><channel>Alert Level</channel><value>2</value><ValueLookup>prtg.customlookups.singleint.alert</ValueLookup></result><text>"+ request.json['alertType'] +" (Device:"+ request.json['deviceMac'] +")</text></prtg>"
        else:
            payload = "<prtg><error>1</error><text>Webhook with unknown alert level: "+ alertLevel +"</text></prtg>"

        #Address different sensors with same port based on the received Meraki alertTypeId. Further differentiation possible e.g. based on device serial etc. 
        alertTypeId = request.json['alertTypeId']

        print("Payload:")
        print(payload)

        if (alertTypeId == "started_reporting" or alertTypeId == "stopped_reporting"):
            post(payload, switch_sensor_token)
        elif(alertTypeId == "power_supply_down" or alertTypeId == "power_supply_up"):
            post(payload, power_sensor_token)
        else:
            print("No matching sensor defined")
        
        return Response(status=200)

#Main Function
if __name__ == "__main__":
    app.run()
