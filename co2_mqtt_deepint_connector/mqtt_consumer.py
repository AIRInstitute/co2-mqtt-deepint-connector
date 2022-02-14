#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import json
import time
import uuid
import paho.mqtt.client as mqtt
from typing import Dict, List, Any

from co2_mqtt_deepint_connector import DeepintProducer, MessageRouter, serve_application_logger


message_limit = 10
message_queue = {}
message_router_ = None

logger = serve_application_logger()


def debug_messages(message, topic):
    import datetime
    import pandas as pd

    try:
        df = pd.read_csv('messages.csv')
    except:
        df = pd.DataFrame(data={'date': [] , 'topic': []})

    new_df = pd.DataFrame(data=[{
        'date': datetime.datetime.now(),
        'topic': topic
    }])

    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv('messages.csv', index=False)


class MQTTConsumer:
    """Consumes from a MQTT list of topics.

    Note: uses the global variables message_limit and message_queue to run.

    Attributes:
        client: connection to MQTT broker.

    Args:
        message_router: performs the mapping between MQTT's topic and Deep Intelligence's source 
        mqtt_broker: MQTT's broker IP.
        mqtt_port: MQTT's broker port.
        mqtt_user: MQTT's broker user.
        mqtt_password: MQTT's broker password.
        mqtt_client_id: MQTT's client id. If not provided, an UUIDv4 will be generated.
        num_message_limit: number of messages to store before dumpt to AIR Institute. If set to 0 each message is send.
    """

    def __init__(self
            , message_router: MessageRouter
            , mqtt_broker: str
            , mqtt_port: int
            , mqtt_user: str
            , mqtt_password: str
            , mqtt_client_id: str = None
            , num_message_limit: int = 10
        ):

        global message_router_, message_limit

        # save producer
        message_router_ = message_router
        message_limit = num_message_limit

        # instance client
        logger.info('Connecting to MQTT')
        mqtt_client_id = f'deepint-connector-{str(uuid.uuid4())}' if mqtt_client_id is None else mqtt_client_id
        
        self.client = mqtt.Client(mqtt_client_id, clean_session =True, protocol=mqtt.MQTTv31)
        self.client.username_pw_set(mqtt_user, password=mqtt_password)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.client.connect(mqtt_broker, keepalive=60, port=mqtt_port)

    @staticmethod
    def _on_connect(client, userdata, flags, rc):
        
        logger.info(f"connected with status code {rc}")
        
        # suscribe to all channels
        client.subscribe('/#')

    @staticmethod
    def _on_message(client: Any, userdata: str, message: Any) -> None:
        """"Consumes messages and dumps it into deepint when real time is set to true.
        """

        try:

            global message_queue, message_limit, message_router_

            # extract data from message
            topic = message.topic
            content = message.payload.decode("utf-8")

            # discard configuration messages
            if 'configuration' in topic or 'update' in topic:
                return

            debug_messages(message=content, topic=topic)

            # discard test device
            if topic == '/CO2_project/123456/mvw2f59w':
                return

            # add message to queue
            if topic not in message_queue:
                message_queue[topic] = []
                logger.info(f'added new topic {topic}')

            message_queue[topic].append(content)

            # dump into deepint if neccesary
            if len(message_queue[topic]) >= message_limit:
                producer = message_router_.resolve(topic)
                if producer is None:
                    logger.warning(f'deleting messages from topic {topic} due to lack of configuration from server')
                else:
                    logger.info(f'sending messages from topic {topic} to deepint.net')
                    producer.produce(data=message_queue[topic])
                message_queue[topic].clear()
        except Excepion as e:
            logger.warning(f'error on message receiving {e}')

    def loop(self) -> None:
        """ Starts the MQTT consumer and produces messages to deepint for undefined time.
        """

        #self.client.loop_start()
        #self.client.loop()
        self.client.loop_forever()

        logger.info('Started consumer')

        # wait into the loop
        while True:
            time.sleep(4)