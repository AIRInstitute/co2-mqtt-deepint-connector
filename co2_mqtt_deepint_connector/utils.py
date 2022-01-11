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
        , mqtt_num_message_limit: int = 10
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
        mqtt_num_message_limit: number of messages to store before dumpt to AIR Institute. If set to 0 each message is send.
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
                , num_message_limit=mqtt_num_message_limit
            )
            consumer.loop()
        except Exception as e:
            raise e
            logger.warning('MQTT connection failed, trying in 5 seconds again ...')
            sleep(5)