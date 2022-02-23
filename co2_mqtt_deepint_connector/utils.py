#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


from time import sleep
from typing import Dict, List, Any

from co2_mqtt_deepint_connector import MessageRouter, MQTTConsumer, serve_application_logger


logger = serve_application_logger()


def connect(
        mqtt_broker: str
        , mqtt_port: int
        , mqtt_user: str
        , mqtt_password: str
        , config_url: str
        , deepint_auth_token: str
        , mqtt_client_id: str = None
        , flush_interval_seconds: int = 10 * 60
    ):
    """Util function to wrap the usage fo message broker, producer and consumer

    Args:
        deepint_auth_token: Authentication token for AIR Institute.
        config_url: the URL of the endpoint used to fetch the mapping (between MQTT and Deep Intelligence) configuration.
        mqtt_broker: MQTT's broker IP.
        mqtt_port: MQTT's broker port.
        mqtt_user: MQTT's broker user.
        mqtt_password: MQTT's broker password.
        mqtt_client_id: MQTT's client id. If not provided, an UUIDv4 will be generated.
        flush_interval_seconds: number of seconds to wait between message queue flushes.
    """

    router = MessageRouter(
            deepint_auth_token=deepint_auth_token
            , config_url=config_url
        )

    while True:
        try:

            consumer = MQTTConsumer(
                message_router=router
                , mqtt_broker=mqtt_broker
                , mqtt_port=mqtt_port
                , mqtt_user=mqtt_user
                , mqtt_password=mqtt_password
                , mqtt_client_id=mqtt_client_id
                , flush_interval_seconds=flush_interval_seconds
            )
            consumer.loop()
        except Exception as e:
            logger.warning(f'MQTT connection failed ({e}), trying in 5 seconds again ...')
            sleep(5)