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

# Login Credentials
For Grafana and InfluxDB 2.0,
<br><b>Username:</b> admin
<br><b>Password:</b> `DOCKER_INFLUXDB_INIT_PASSWORD`