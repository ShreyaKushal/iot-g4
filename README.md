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

</t><ul>
    <li>Go to Node-RED</li>
    <li>Double click on 'influxdb out node'</li>
    <li>Under Server, click on the pencil icon</li>
    <li>Copy the `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` value from <i>.env</i> file and paste under Token</li>
</ul>

4. Configure Grafana
   `</t>`

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
         - Add Dashboard Link > *Any Title* > Type: Link > URL: http://localhost:8686/api/v5/report/`\<Dashboard uID\>`?apitoken=`<Service Account API Token\>` <br>
         - Options: <br>
           - [x] Include current time range <br>
           - [x] Include current template variable values <br>
         - Apply <br>
         - Save Dashboard <br>
    </li>

</ul>

# Login Credentials

For Grafana and InfluxDB 2.0,
`<br><b>`Username:`</b>` admin
`<br><b>`Password:`</b>` `DOCKER_INFLUXDB_INIT_PASSWORD`
