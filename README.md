# GVE_DevNet_Meraki_PRTG_Integration
Meraki Integration for PRTG Network Monitor via:
* SNMP
* REST API
* Webhook

for local and remote networks.

## Contacts
* Ramona Renner

## Solution Components
* Meraki
* PRTG Network Monitor

## Pre-requisites

* Meraki Dashboard access
* Meraki Dashboard API key (instructions shared in this document later)
* One Meraki network (with local and remote access) or two separate Meraki networks (one local and one remote)
* PRTG Web-interface

This documentation describes ways to integrate Meraki and PRTG via SNMP, REST API and Webhook in a compact and step-by-step manner. Links for more detailed instructions and additional information can be found in the section [further resources](#further-resources) at the bottom of this page.


| :information_source: Update              |
|:-----------------------------------------|
| These instructions describe the process used for a PoV in April 2021. PRTG and Meraki are constantly developing their products and thereby simplified the described process by now. More details can be found in the corresponding sections. |


## Table of contents

1. [Download Repository Files and Create Environment](#download-repository-files-and-create-environment)

2. [SNMP](#snmp)

    2.1 [Preparation for SNMP Setup](#preparation-for-snmp-setup)

    2.2 [SNMP for Local Network with Device Template](#snmp-for-local-network-with-device-template)

    2.3 [SNMP for Remote Network with Device Template](#snmp-for-remote-network-with-device-template)

    2.4 [SNMP for Local Network without Device Template](#snmp-for-local-network-without-device-template)

3. [REST API](#rest-api)

    3.1 [Preparation for REST API Setup](#preparation-for-rest-api-setup)

    3.2 [REST API for Local and Remote Network](#rest-api-for-local-and-remote-network)

4. [Webhook](#webhook)

    4.1 [Webhook for Local and Remote Network](#webhook-for-local-and-remote-network)

5. [Further Resources](#further-resources)


## Download Repository Files and Create Environment

This section describes how to download the required files and how to create an environment to run a translation script for the [Webhook](#webhook) integration. 
    
Via CLI e.g. Terminal(MAC) or Git Bash(Windows):
1. Iterate to the preferred directory
    ```python
    cd [preferred path] 
    ```

2.	Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html)).

3. Access the created virtual environment folder
    ```python
    cd [add name of virtual environment here] 
    ```

4.	Clone this Github repository into the virtual environment folder
    ```python
    git clone [add github link here]
    ```
    For the Github link: 

    In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**

    ![/IMAGES/0image.png](/IMAGES/giturl.png)

5. Access the folder **GVE_DevNet_Meraki_PRTG_Integration**
    ```python
    cd GVE_DevNet_Meraki_PRTG_Integration

    ```
The folder **GVE_DevNet_Meraki_PRTG_Integration** includes the mentioned files.



## SNMP 

Simple Network Management Protocol (SNMP) allows network administrators to query devices for various information. Meraki allows SNMP polling to gather information either from the dashboard or directly from MR access points, MS switches, and MX security appliances. Third party network monitoring tools can use SNMP to monitor certain parameters.

Meraki devices support the majority of OIDs located within the subset of the following MIBs: 

    SNMPv2-MIB .1.3.6.1.2.1.1
    IF-MIB .1.3.6.1.2.1

These MIBs are not proprietary and therefore are available on most network monitoring systems.

Additional Meraki specific information can be found in the MERAKI-CLOUD-CONTROLLER-MIB, which is located under **Organization** > **Settings** > **SNMP**. Please note that this MIB is used to poll Dashboard, not Meraki devices locally. Please reference the Standard MIBs above for options when polling local devices.


### Preparation for SNMP Setup 

Follow the steps in this section to import a Meraki device template and lookup files to PRTG.

In the PRTG's Program directory (by default **C:\Program Files (x86)\PRTG Network Monitor**),  

1. Copy the **devicetemplates\Meraki.odt** file from the repository folder into the PRTG **devicetemplates** subfolder  

2. Copy the **lookups\oid.meraki-cloud-controller-mib.dev.devstatus.ovl** file from the repository folder into the PRTG **lookups\custom** subfolder
    
      
In the PRTG Web-interface,  

1. Go to **Setup** > **Administrative Tools**  

2. Press **Go** in the **Load Lookups and File List** section  

    ![/IMAGES/PRTG_load_lookup.png](/IMAGES/PRTG_load_lookup.png)

The two mentioned files were created and published by Paessler ([Reference](https://kb.paessler.com/en/topic/59986-help-monitoring-meraki-network#reply-232609)).


### SNMP for Local Network with Device Template

In this scenario, we will poll information directly from the Meraki devices. The SNMP traffic will stay within the local network - thereby, each device needs to be reachable via local IP address.  

In the following, we will use a device template to automatically add sensors. 
In case you didn't import the device template and lookup file to PRTG yet, follow the steps described in the section [Preparation for SNMP Setup](#preparation-for-snmp-setup) before continuing.


*Configure local SNMP polling in the Meraki Dashboard:*  
In the Meraki Dashboard,
1. Go to **Network-wide** > **General** > **Section: Reporting** 
2. Enable SNMP by selecting a version via **SNMP access** field e.g. **V1/V2c (community string)**
3. Enter a preferred **community string**

    ![/IMAGES/Meraki_direct_SNMP_polling.png](/IMAGES/Meraki_direct_SNMP_polling.png)

4. Click **Save**  
  
  
*Create a PRTG group that configures SNMP:*  
In the PRTG Web-interface,  
1. Select **Devices** > **Add Group** in the main menu bar  
2. In the appearing dialog, select a preferred parent > **Ok**  
3. Enter a group name e.g. **SNMP in Local Network with device template**  
4. Define the SNMP group settings in the **Credentials for SNMP Devices** section:

    5.1 Turn off the **inherit from (parent)** option

    5.2 Select the same SNMP **version** as previously defined in the Meraki Dashboard e.g. **SNMP v2c (recommended)** 

    5.3 Enter the **community string** previously defined in the Meraki Dashboard

    5.4 Enter SNMP **Port: 161**  
    
    ![/IMAGES/PRTG_direct_SNMP_polling_group.png](/IMAGES/PRTG_direct_SNMP_polling_group.png)

6. Click **Save**  
  

*Add a PRTG device for each Meraki device:*  
In the PRTG Web-interface,  
1. Select the **Add Device** option in the context menu of the group created in the last section
2. Enter a device name e.g. **MS120-8LP - xx:xx:xx:xx:xx:xx**
3. Enter the local IP address of the Meraki device in the **IPv4 Address/DNS Name** field. (The IP address is listed on the device detail page in the Meraki Dashboard)
4. In the **Device Identification and Auto-Discovery** section:  

    4.1. Select the option **Auto-discovery with specific device templates** 

    4.2. Select the **Device Template: Custom Meraki**

    ![/IMAGES/SNMP_local_add_device.png](/IMAGES/SNMP_local_add_device.png)
    

5. Click **Save**  

PRTG will now start the auto-discover process. On successful discovery, PRTG automatically adds multiple sensors. 
Repeat step 1.-5. for each Meraki device.  

**Example result:**  
![/IMAGES/result_SNMP_local_template.png](/IMAGES/result_SNMP_local_template.png)
![/IMAGES/result_SNMP_local_template_sensor.png](/IMAGES/result_SNMP_local_template_sensor.png)

    

### SNMP for Remote Network with Device Template

In this scenario, we will poll information via SNMP over the Meraki Dashboard. 

In the following, we will use a device template to automatically add sensors. 
In case you didn't import the device template and lookup file to PRTG yet, follow the steps described in the section [Preparation for SNMP Setup](#preparation-for-snmp-setup) before continuing.


*Configure SNMP polling in the Meraki Dashboard:*  
In the Meraki Dashboard,   
1. Go to **Organization** > **Settings** > **SNMP**  
2. Enable the preferred SNMP version by changing the corresponding field to enabled. e.g. **SNMP V2C enabled**

    ![/IMAGES/Meraki_dashboard_SNMP_polling.png](/IMAGES/Meraki_dashboard_SNMP_polling.png)

3. Click **Save** 

Once SNMP has been enabled, you will be able to send the SNMP requests to the host that is defined directly under the enable setting. It also defines the community string and provides a sample command to extract information via SNMP requests.   


*Create a PRTG group that configures SNMP:*   
In the PRTG Web-interface,  
1. Select **Devices** > **Add Group** in the main menu bar
2. In the appearing dialog, select a preferred parent > **Ok** 
3. Enter a group name e.g. **SNMP in Remote Network with device template**
4. Define the SNMP group settings in the **Credentials for SNMP Devices** section:

    4.1 Turn off the **inherit from (parent)** option

    4.2 Select the same SNMP **version** as previously enabled in the Meraki Dashboard e.g. **SNMP v2c (recommended)** 

    4.3 Enter the **Community String** as displayed in the Meraki Dashboard

    4.4 Enter SNMP **Port: 16100** 

    ![/IMAGES/PRTG_dashboard_SNMP_polling_group.png](/IMAGES/PRTG_dashboard_SNMP_polling_group.png)

8. Click **Save**  


*Add **one** PRTG device for all Meraki devices:*      
In the PRTG Web-interface,   

1. Select **Add Device** in the context menu of the group created in the last section
2. Enter a device name e.g. **Meraki Devices via Dashboard**
3. Enter **snmp.meraki.com** in the **IPv4 Address/DNS Name** field  
    
    In the **Device Identification and Auto-Discovery** section,
4. Select the option **Auto-discovery with specific device templates** 
5. Select the **Device Template: Custom Meraki**

    ![/IMAGES/SNMP_remote_add_device.png](/IMAGES/SNMP_remote_add_device.png)
  
6. Click **Save**  
  
PRTG will now start the auto-discover process and thereby automatically add sensors to the PRTG device.


| :warning: Attention                      |
|:-----------------------------------------|
| After the automatic discovery process, all sensor names start with **Meraki AP**. The actual device type can differ from this naming. Compare the serial number in the sensor page header to identify the actual device type and adapt the sensor name manually.  |



**Example result:**  
    ![/IMAGES/result_SNMP_remote_template.png](/IMAGES/result_SNMP_remote_template.png)
    ![/IMAGES/result_SNMP_remote_template_sensor.png](/IMAGES/result_SNMP_remote_template_sensor.png)


## SNMP for Local Network without Device Template

In this scenario, we will again poll information directly from the Meraki devices. The SNMP traffic will stay within the local network - thereby, each device needs to be reachable via local IP address.  
This time we will add the SNMP sensors manually instead of using the Meraki Template. 

*Configure SNMP polling in the Meraki Dashboard: (if not done in the previous section)*  
In the Meraki Dashboard,
1. Go to **Network-wide** > **General** > **Section: Reporting** 
2. Enable SNMP by selecting a version via **SNMP access** field e.g. **V1/V2c (community string)**
3. Enter a preferred **community string**

    ![/IMAGES/Meraki_direct_SNMP_polling.png](/IMAGES/Meraki_direct_SNMP_polling.png)

4. Click **Save**  
  
  
*Create a PRTG group that configures SNMP:*  
In the PRTG Web-interface,  
1. Select **Devices** > **Add Group** in the main menu bar  
2. In the appearing dialog, select a preferred parent > **Ok**  
3. Enter a group name e.g. **SNMP in Local Network without template**  
4. Define the SNMP group settings in the **Credentials for SNMP Devices** section:

    5.1 Turn off the **inherit from (parent)** option

    5.2 Select the same SNMP **version** as previously defined in the Meraki Dashboard e.g. **SNMP v2c (recommended)** 

    5.3 Enter the **community string** previously defined in the Meraki Dashboard

    5.4 Enter SNMP **Port: 161**  
    
    ![/IMAGES/PRTG_direct_SNMP_polling_group.png](/IMAGES/PRTG_direct_SNMP_polling_group.png)

6. Click **Save**  
  

*Add a PRTG device for each Meraki device:*   
In the PRTG Web-interface,  
1. Select the **Add Device** option in the context menu of the group created in the last section
2. Enter a device name e.g. **MS120-8LP - xx:xx:xx:xx:xx:xx**
3. Enter the local IP address of the Meraki device in the **IPv4 Address/DNS Name** field. (The IP address is listed on the device detail page in the Meraki Dashboard)
4. Click **Save**  
    
    ![/IMAGES/SNMP_local_add_device_manually.png](/IMAGES/SNMP_local_add_device_manually.png) 

Repeat step 1.-4. for each Meraki device.


*Add a PRTG sensor:*  
In the PRTG Web-interface,  
1. Select **Add Sensor** in the context menu of a created device
2. Search and select the **SNMP custom advanced** sensor from the list
3. Fill in the preferred **Sensor Name**, **Channel Name**, **Channel OID** and **Channel Unit** e.g. **Manual SNMP sensor**, **devInterfaceRecvPkts**, **1.3.6.1.2.1.31.1.1.1.10.2** and **Count** 

    ![/IMAGES/SNMP_local__add_sensor_manually.png](/IMAGES/SNMP_local_add_sensor_manually.png)  

4. Click **Create**  


**Example Result:**  
    ![/IMAGES/result_SNMP_local_without_template.png](/IMAGES/result_SNMP_local_without_template.png)
    ![/IMAGES/result_SNMP_remote_without_template_sensor.png](/IMAGES/result_SNMP_remote_without_template_sensor.png)



## REST API

Meraki offers a RESTful API to programmatically manage and monitor Meraki networks at scale. The wide range of all Meraki Dashboard endpoints are documented [here](https://developer.cisco.com/meraki/api-v1).

### Preparation for REST API Setup

Follow the steps in this section to retrieve a Meraki API key, an organization ID and a device serial number. All three are required for the following steps. 

1. Obtain and note the Meraki API Key by following the instructions [here](https://developer.cisco.com/meraki/api/#!authorization/obtaining-your-meraki-api-key).

2. To obtain and note the **Organization ID** execute the following steps: 
    
    2.1 Go to https://developer.cisco.com/meraki/api-v1/#!get-organizations > click **Configuration**
        ![/IMAGES/0image.png](/IMAGES/editor1.png)

    2.2 Add the Meraki Api key from step 1 in the **APIKey in header** field > press **Save**
        ![/IMAGES/0image.png](/IMAGES/editor2.png)

    2.3 Click **Run** and note the returned organization ID  
        ![/IMAGES/0image.png](/IMAGES/editor3.png)

3. To obtain and note the **serial number** of a Meraki switch in the Meraki Dashboard:
    
    3.1 Go to **Switch** > **Switches** > **[Switch name]**

    3.2 Find serial number on the left side under **SERIAL NUMBER**


### REST API for Local and Remote Network 

In this scenario, we will poll information via REST API. Thereby, we will create different sensors manually.   

In the following, we will use a Meraki API key, an organization ID and a device serial number. In case you didn't retrieve this information yet, follow the steps described in the section [Preparation for REST API setup](#preparation-for-rest-api-setup) before continuing.  

*Create a PRTG group (optionally):*   
In the PRTG Web-interface,  
1. Select **Devices** > **Add Group** in the main menu bar  
2. In the appearing dialog, select a preferred parent > **Ok**  
3. Enter a group name e.g. **REST API**  
 
  
*Add a PRTG device:*  
In the PRTG Web-interface,    
1. Select **Add Device** in the context menu of the group created in the last section
2. Enter a device name e.g. **MS120-8LP - xx:xx:xx:xx:xx:xx**
3. Enter **api.meraki.com/api/v1** in the **IPv4 Address/DNS Name** field  

    ![/IMAGES/rest_add_device.png](/IMAGES/rest_add_device.png)

4. Click **Save**  


This documentation covers two sensors for an integration via REST API - the **Python sensor** and **REST sensor**. In the following, instructions for both sensors are listed. Choose the preferred option. 


**Add a PRTG Python sensor for the [Get Organization Devices Statuses Endpoint](https://developer.cisco.com/meraki/api-v1/#!get-organization-devices-statuses):**    
1. Prepare the python file:  

    1.1. Open the **rest.py** file from the repository folder **customsensor/python** in an editor

    1.2. Fill in the **apikey**, **serial** and **organizationid** (see [Add here ...] placeholders) based on the obtained values from the [Preparation for REST API setup](#preparation-for-rest-api-setup) section 

    ![/IMAGES/rest_py_file.png](/IMAGES/rest_py_file.png)  

    1.3 Copy the python file to the PRTG's Program directory (default **C:\Program Files (x86)\PRTG Network Monitor**) into the **Custom Sensor/python** subfolder  
    
    In the PRTG Web-interface,  
2. Go to **Setup** > **Administrative Tools**
3. Press **Go** in the **Load Lookups and File List** section  

    ![/IMAGES/PRTG_load_lookup.png](/IMAGES/PRTG_load_lookup.png)

4. Select **Add Sensor** from the context menu of a created device
5. Search and select the **Python Script Advanced** sensor from the list
6. Fill in a sensor name e.g. **MS120 online** and select **rest.py** in the **Python Script** field  

    ![/IMAGES/rest_add_python_sensor.png](/IMAGES/rest_add_python_sensor.png)  

7. Click **Create**  



**Add a PRTG REST sensor for the [Get Device Switch Ports Statuses Endpoint](https://developer.cisco.com/meraki/api-v1/#!get-device-switch-ports-statuses):**  
1. Prepare the template file:  

    1.1. Open the **merakicustomportstatus.template** file from the repository folder **customsensor/rest**

    1.2. Input the **portnumber** (see **[Add here port number]** placeholders). Attention: the port count starts with 0, thereby input 0 for port 1, 1 for port 2 etc.

    ![/IMAGES/rest_sensor_file.png](/IMAGES/rest_sensor_file.png)  

    1.3 Copy the template file to the PRTG's Program directory (default **C:\Program Files (x86)\PRTG Network Monitor**) into the **Custom Sensor/rest** folder

    In the PRTG Web-interface,  
2. Go to **Setup** > **Administrative Tools**
3. Press **Go** in the **Load Lookups and File List** section  

    ![/IMAGES/PRTG_load_lookup.png](/IMAGES/PRTG_load_lookup.png)  

4. Select **Add Sensor** in the context menu of a created device
5. Search and select the **REST custom** sensor from the list
6. Define the settings in the **REST Specific** section:

    6.1. Fill in a sensor name e.g. **Port 1**

    6.2. Select **Request Method: GET**

    6.3. Select **Request Protocol: HTTPS**

    6.4. Select **HTTP Headers: USE custom HTTP headers**

    6.5. Fill in the **HTTP Headers** field with **X-Cisco-Meraki-API-Key:[your Meraki API key]**

    6.6. Fill in the **REST Query** field with an endpoint e.g. **/devices/[preferred serial number]/switch/ports/statuses**

    ![/IMAGES/PRTG_rest_custom_settings.png](/IMAGES/PRTG_rest_custom_settings.png)

    6.6. Choose the corresponding **REST Configuration** e.g. **merakicustomportstatus.template**

7. Define a sensor dependency in the **Schedules, Dependencies, and Maintenance Windows** section:  

    7.1 Select the **Dependency Type: Select a sensor**  

    7.2 Select the **Python Rest Sensor** created in the last section as **Dependency**

    ![/IMAGES/rest_dependency.png](/IMAGES/rest_dependency.png)

7. Click **Create**


| :information_source: Update              |
|:-----------------------------------------|
| PRTG recently released a REST Sensor v2 that simplifies the described process. |

**Example Result:**  
    ![/IMAGES/rest_result_overview.png](/IMAGES/rest_result_overview.png)
    ![/IMAGES/rest_result_python_sensor.png](/IMAGES/rest_result_python_sensor.png)
    ![/IMAGES/rest_result_rest_sensor.png](/IMAGES/rest_result_rest_sensor.png)



## Webhook

Meraki webhooks are a powerful and lightweight way to subscribe to alerts sent from the Meraki Cloud when something happens. They include an API style message in machine and human-readable JSON, and are sent to a unique URL where they can be processed, stored or used to trigger powerful automations.

### Webhook for Local and Remote Network 

For the webhook integration, a simple, custom translation script/app for switch online/offline or switch power supply up/down alerts, is used. The app requires to be reachable over an internet accessible URL. Therefore, it can be deployed on different IaaS platforms like Heroku, Amazon Web Services Lambda, Google Cloud Platform (GCP) etc. . For simplicity, we use the tool ngrok here.


*Create a PRTG group (optionally):*   
In the PRTG Web-interface,  
1. Select **Devices** > **Add Group** in the main menu bar
2. In the appearing dialog, select a preferred parent > **Ok** 
3. Enter a group name e.g. **Webhook**
 
  
*Add a PRTG device:*  
In the PRTG Web-interface,    
1. Select **Add Device** in the context menu of the group created in the last section
2. Enter a device name e.g. **MS120-8LP - xx:xx:xx:xx:xx:xx**
3. Enter the **public device IP** in the **IPv4 Address/DNS Name** field - only because this field requires an input (The IP address is listed on the device detail page in the Meraki Dashboard)

    ![/IMAGES/webhook_device.png](/IMAGES/webhook_device.png)

4. Click **Save**  


*Prepare and run the translation script/app:*  
1. Download ngrok on the [official website](https://ngrok.com/download).
2. Extract the folder files 
3. Run the **ngrok.exe** by double-clicking on the file
4. Type the command **ngrok http 5000** and press enter
5. Note the https redirect URL    

    ![/IMAGES/ngrok.png](/IMAGES/ngrok.png)

    
*Configure the Webhook in the Meraki Dashboard:*  
In the Meraki Dashboard,  
1. Go to **Network-wide** > **Alerts**
2. Add an HTTP server in **Webhooks: HTTP servers** section:  

    2.1. Fill in a **name** for your webhook e.g. **PRTG Integration**  

    2.2. Add **[ngrok https url]/webhook** in the **URL** field  
    
    2.3. Choose and fill in a **shared secret** e.g. **testwebhook**    

    ![/IMAGES/merakiwebhook.png](/IMAGES/merakiwebhook.png)  

3. Enable a switch alert in the **Switch section**:   

    4.1. Check the **A switch goes offline for x minutes** option and choose the preferred time e.g.**5**  

    ![/IMAGES/webhook_switch_alert.png](/IMAGES/webhook_switch_alert.png) 


5. Add the HTTP server as **Default recipients** by typing the HTTP server name e.g. **Webhook: PRTG Integration** into the corresponding field

6. Click **Save**


*Create HTTP Push Sensor:*  
In the PRTG Web-interface,  
1. Select **Add Sensor** in the context menu of a created device
2. Search and select the **HTTP Push Data Advanced** sensor from the list
3. Define the settings in the **HTTP Push** section:

    3.1. Fill in the name of the sensor e.g. **Webhook - Switch online/offline** or **Webhook - Switch Power supply up/down**

    3.2. Select **SSL/TLS Settings: HTTP**

    3.3. Select **Request Method: POST**  

    ![/IMAGES/httppush.png](/IMAGES/httppush.png)

4. Click **Create**
5. Open the sensor settings view by clicking on **[sensor name]** > **Settings**
6. Note the **Identification Token** and **Port** for later

    ![/IMAGES/webhook_identifier.png](/IMAGES/webhook_identifier.png)  


Create a second sensor by following the steps 1.-6. again. The first sensor is for the **stopped_reporting/started_reporting** and second for the **power_supply_down/power_supply_up** alert.


*Prepare and run the script/app:*  
1. Open the **backend.py** file from the repository folder **webhook**
2. Input the sensor identification tokens, webhook secret and port (see [Add here ...] placeholders) from the previous sections
3. Run the script via the command **python backend.py**


*Trigger the webhooks:*  
In the Meraki Dashboard,   
1. Trigger a **power_supply_down** alert:  

    1.1. Go to **Network-wide** > **Configure** > **Alerts**  

    1.2. Click **Send test webhook** in the **Webhooks: HTTP servers** section

    ![/IMAGES/httppush.png](/IMAGES/httppush.png)  

2. Trigger a **stopped_reporting** alert by unplugging the switch and a **started_reporting** alert by plugging it in again.


| :information_source: Update              |
|:-----------------------------------------|
| Update: Meraki now offers a Webhook-Template feature and builder (currently as beta) that simplifies the described process. More information can be found in the Meraki [Developer Hub](https://developer.cisco.com/meraki/webhooks/#!payload-templates/webhook-payload-templates). The webhook builder is available [here](https://webhook-builder-vpfmunhy6a-uc.a.run.app/). |

**Example Result:**  
    ![/IMAGES/webhook_result.png](/IMAGES/webhook_result.png)
    ![/IMAGES/webhook_switch_power_off.png](/IMAGES/webhook_switch_power_off.png)
    ![/IMAGES/webhook_switch_alert_online.png](/IMAGES/webhook_switch_alert_online.png)


## Further resources 

More detailed instructions for the mentioned steps can be found on the following official developer documentation pages:

### PRTG General:
* [Add a PRTG group](https://www.paessler.com/manuals/prtg/add_a_group)
* [Add a PRTG device](https://www.paessler.com/manuals/prtg/add_a_device)
* [Add a Sensor](https://www.paessler.com/manuals/prtg/add_a_sensor)

### SNMP
* [Meraki SNMP Overview and Configuration](https://documentation.meraki.com/General_Administration/Monitoring_and_Reporting/SNMP_Overview_and_Configuration)
* [Paessler's Instructions on Meraki Integration via SNMP](https://kb.paessler.com/en/topic/59986-help-monitoring-meraki-network#reply-232609)
* [SNMP Custom Advanced Sensor](https://www.paessler.com/manuals/prtg/snmp_custom_advanced_sensor)

### REST API:
* [Meraki Dashboard API Documentation](https://developer.cisco.com/meraki/api-v1)
* [Python Script Advanced Sensor](https://www.paessler.com/manuals/prtg/python_script_advanced_sensor)
* [REST Custom Sensor](https://www.paessler.com/manuals/prtg/rest_custom_sensor)

### Webhook
* [Meraki Webhooks](https://developer.cisco.com/meraki/webhooks/#!introduction/)
* [HTTP Push Data Advanced Sensor](https://www.paessler.com/manuals/prtg/http_push_data_advanced_sensor)
* [Meraki Webhook-Template Feature (beta)](https://developer.cisco.com/meraki/webhooks/#!payload-templates/webhook-payload-templates)
* [Webhook Builder (beta)](https://webhook-builder-vpfmunhy6a-uc.a.run.app/)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
