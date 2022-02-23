#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.

# install newer version
sudo python3 -m pip install . --upgrade

# define parameters
MQTT_BROKER="212.128.140.74"
MQTT_PORT="2780"
MQTT_USER="bisite"
MQTT_PASSWORD="bisite00"
CONFIG_URL="http://212.128.140.74:8080/api/v1/co2/devices/info"
DEEPINT_AUTH_TOKEN="JKM1wuXItbZ0JRF8ZdaNE6PW9iGmND2_Kyq2KVnG1MIPch_czSLXC1N24GLWjAZszI4eQrQuxRvdUxsNtF0KLw"
MQTT_CLIENT_ID=""
NUM_SECONDS_QUEUE_FLUSH="600"
QUIET_MODE_SET="False"

# run connector
sudo co2-mqtt-deepint-connector "${MQTT_BROKER}" "${MQTT_PORT}" "${MQTT_USER}" "${MQTT_PASSWORD}" "${CONFIG_URL}" "${DEEPINT_AUTH_TOKEN}" "${MQTT_CLIENT_ID}" "${NUM_SECONDS_QUEUE_FLUSH}" "${QUIET_MODE_SET}"
