#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.

# install newer version
sudo python3 -m pip install . --upgrade

# define parameters
MQTT_BROKER="localhost"
MQTT_PORT="2780"
MQTT_USER="bisite"
MQTT_PASSWORD="bisite00"
CONFIG_URL="http://localhost:8080/api/v1/co2/devices/info"
DEEPINT_AUTH_TOKEN="bpZgeQ7qqmwbr04ux4-oCfv5fk1o4ApVRT8o3Wi4CiowfuQDvpC2X2Uqohnc3htHcUwca0g_ldpGIK4MeQFZEw"
MQTT_CLIENT_ID=""
NUM_SECONDS_QUEUE_FLUSH="600"
QUIET_MODE_SET="False"

# run connector
sudo co2-mqtt-deepint-connector "${MQTT_BROKER}" "${MQTT_PORT}" "${MQTT_USER}" "${MQTT_PASSWORD}" "${CONFIG_URL}" "${DEEPINT_AUTH_TOKEN}" "${MQTT_CLIENT_ID}" "${NUM_SECONDS_QUEUE_FLUSH}" "${QUIET_MODE_SET}"
