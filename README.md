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

# Login Credentials

For Grafana and InfluxDB 2.0,
`<br><b>`Username:`</b>` admin
`<br><b>`Password:`</b>` `DOCKER_INFLUXDB_INIT_PASSWORD`
