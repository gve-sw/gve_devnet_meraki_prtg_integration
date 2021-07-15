# -*- coding: utf-8 -*-
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

import json
import sys
import urllib.request as urllib

from prtg.sensor.result import CustomSensorResult
from prtg.sensor.units import ValueUnit


if __name__ == "__main__":
    try:

        req = urllib.Request("https://api.meraki.com/api/v1/organizations/[Add here orga id]/devices/statuses")
        req.add_header("Content-Type", "application/xml")
        req.add_header("X-Cisco-Meraki-API-Key", "[Add here API key]")
        webURL = urllib.urlopen(req)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        devices = json.loads(data.decode(encoding))

        for device in devices:

            if(device['serial'] == "[Add here serial number]"):
                if(device['status'] == "online"):

                    json_result = '''{
                                    "prtg": {
                                    "text":"Das Gerät [Add here serial number] ist online",
                                    "result": [
                                        {
                                        "channel": "Online",
                                        "value": 1,
                                        "Unit": "Custom",
                                        "ValueLookup": "prtg.standardlookups.boolean.statetrueok"
                                        }
                                    ]
                                    }
                                    }'''
                                    
                    break

                else:
                    json_result = ''' {
                                    "prtg": {
                                    "error": 1,
                                    "text": "Das Gerät [Add here serial number] ist offline"
                                    }
                                    }'''
                    
        print(json_result)

        
    except Exception as e:
        json_result = ''' {
                        "prtg": {
                        "error": 1,
                        "text": "Fehler bei der Scriptausführung"
                        }
                        }''' 
        print(json_result)