# Getting Started

1. Open the Terminal.
2. Build image for Node-RED to automatically load the required flow.

```
docker build -t nodered-image .
```

2. Execute the following command.

```
docker compose up
```

3. Configure Node-RED
<ul>
    <li>Go to Node-RED</li>
    <li>Double click on 'influxdb out node'</li>
    <li>Under Server, click on the pencil icon</li>
    <li>Copy the `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` value from <i>.env</i> file and paste under Token</li>
</ul>

4. Configure Grafana
<ul>
    <li>
        Log in with a temporary credential:
        <br><b>Username:</b> admin
        <br><b>Password:</b> admin 
    </li>
    <li>
        When prompted to change the password, change to `DOCKER_INFLUXDB_INIT_PASSWORD`
    </li>
    <li>
        Add influxdb as data source using Flux
    </li>
    <li>
        Basic Auth Details: refer to Login Credentials below
    </li>
    <li>
        InfluxDB Details:
        <ul>
            <li>
                Organisation: iot-g3
            </li>
            <li>
                Token: `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`
            </li>
            <li>
                Default Bucket: iaq-data
            </li>
        </ul>
    </li>
</ul>

5. Create Service account to allow Grafana Report generator to use tokenID parameter
<ul>
    <li>
        Create Service account to get API token: <br>
        - Home > Administration > Users and access > Service accounts <br>
         - Add service account > *Fill in details* > Add service account token <br>
         - Display name (choose to set or auto) > Expiration: No expiration > Generate token > Copy clipboard > paste somewhere to save <br>
    </li>
    <li>
       Create report generation link in dashboard: <br>
       - Home > Dashboards > *Dashboard of choice* > Dashboard settings > Links <br>
         - Add Dashboard Link > *Any Title* > Type: Link > URL: http://localhost:8686/api/v5/report/ `Dashboard uID` ?apitoken= `Service Account API Token` <br>
         - Options: <br>
           - [x] Include current time range <br>
           - [x] Include current template variable values <br>
         - Apply <br>
         - Save Dashboard <br>
    </li>
</ul>

6. Configure Home Assistant
<ul>
    <li>Set up user
        <ul>
            <li>Click on 'CREATE MY SMART HOME' button</li>
            <li>
                Key in the details as follows (refer to the <i>.env</i> file):
                <ul>
                    <li><b>Name: </b> `HOME_ASSISTANT_USERNAME`</li>
                    <li><b>Password: </b> `HOME_ASSISTANT_PASSWORD`</li>
                    <li><b>Confirm password: </b> `HOME_ASSISTANT_PASSWORD`</li>
                </ul>
                Click 'Next'
            </li>
            <li>Search address: 'Singapore, Singapore' and click 'Next'</li>
            <li>Click 'Next' again and click 'Finish'</li>
        </ul>
    </li>
    <li>Link Tuya device
        <ul>
            <li>Go to Settings > Devices & services > Add integration > Tuya</li>
            <li><b>User code: </b>`TUYA_USER_CODE`</li>
            <li>Use Tuya Smart app to scan QR code > Submit > Finish</li>
        </ul>
    </li>
    <li>Set up MQTT broker
        <ul>
            <li>Go to Settings > Devices & services > Add integration > MQTT > MQTT</li>
            <li>Key in the following details:
                <ul>
                    <li><b>Broker: </b>test.mosquitto.org</li>
                    <li><b>Port: </b> 1883</li>
                </ul>
            </li>
            <li>Click Submit > Finish</li>
            <li>Select MQTT > Configure > Under Listen to a topic,  subscribe to 'iot/sensor1', select 2 as the QoS > Start Listening</li>
        </ul>
    </li>
    <li>Automate Tuya device based on message received on a MQTT topic
        <ul><li>Turn on Tuya device</li>
                <ul>
                    <li>Go to Settings > Automations & scenes > Create Automation > Create new automation</li>
                    <li>Under 'When', click Add Trigger > Other triggers > MQTT
                        <ul>
                            <li><b>Topic: </b> iot/sensor1/on</li>
                        </ul>
                    </li>
                    <li>Under 'Then do', click Add Action > Device
                        <ul>
                            <li><b>Device: </b> Smart socket</li>
                            <li><b>Action: </b> Turn on Smart Socket 1</li>
                        </ul>
                    </li>
                    <li>Click Save</li>
                    <li>Name the automation as 'TurnOnRequest' and Save</li>
                </ul>
                <li>Turn off Tuya device</li>
                <ul>
                    <li>Go to Settings > Automations & scenes > Create Automation > Create new automation</li>
                    <li>Under 'When', click Add Trigger > Other triggers > MQTT
                        <ul>
                            <li><b>Topic: </b> iot/sensor1/off</li>
                        </ul>
                    </li>
                    <li>Under 'Then do', click Add Action > Device
                        <ul>
                            <li><b>Device: </b> Smart socket</li>
                            <li><b>Action: </b> Turn off Smart Socket 1</li>
                        </ul>
                    </li>
                    <li>Click Save</li>
                    <li>Name the automation as 'TurnOffRequest' and Save</li>
                </ul>
        </ul>
    </li>
    <li>To test, run <i>tuya.py</i></li>
</ul>

7. Set up ai-service
<ul>
    <li>Copy template file to templates_volume after container start:</li>
    <ul>
        <li>Run <i>docker container ls</i></li>
        <li>Look for iot-g3-ai-service and copy the <i>CONTAINER ID</i></li>
        <li>In the iot-g3 directory,
            Run <i>docker cp template.tex 
                <b>{CONTAINER_ID}:/var/lib/ai-service/templates/template.tex</b>
            </i>
        </li>
    </ul>
</ul>

# Login Credentials

For Grafana and InfluxDB 2.0,
<br><b>Username: </b>`admin`
<br><b>Password: </b>`DOCKER_INFLUXDB_INIT_PASSWORD`
