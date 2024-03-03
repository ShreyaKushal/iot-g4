FROM nodered/node-red:latest

RUN npm install node-red-contrib-influxdb node-red-contrib-telegrambot
COPY flows.json /data/flows.json
