#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import json
import time
import uuid
import datetime
import paho.mqtt.client as mqtt
from typing import Dict, List, Any

from co2_mqtt_deepint_connector import DeepintProducer, MessageRouter, serve_application_logger



message_queue = {}
message_router_ = None
flush_interval = None
last_queue_flush = datetime.datetime.now()

logger = serve_application_logger()


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
        flush_interval_seconds: number of seconds to wait between message queue flushes.
    """

    def __init__(self
            , message_router: MessageRouter
            , mqtt_broker: str
            , mqtt_port: int
            , mqtt_user: str
            , mqtt_password: str
            , mqtt_client_id: str = None
            , flush_interval_seconds: int = 10 * 60
        ):

        global message_router_, flush_interval

        # save producer
        message_router_ = message_router
        flush_interval = datetime.timedelta(seconds=flush_interval_seconds)

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

            global message_queue, last_queue_flush, flush_interval, message_router_

            # extract data from message
            topic = message.topic
            content = message.payload.decode("utf-8")

            # discard configuration messages
            if 'configuration' in topic or 'update' in topic or topic == '/CO2_project/123456/mvw2f59w':
                return

            # add message to queue
            org = topic.split('/')[1]
            if org not in message_queue:
                message_queue[org]= []
                
            message_queue[org].append({
                'topic': topic,
                'content': content
            })

            # flush if neccesary
            now = datetime.datetime.now()
            if (now - last_queue_flush) >= flush_interval:

                last_queue_flush = now
                messages, message_queue = message_queue, {}

                for topic in messages:
                    producer = message_router_.resolve(topic)
                    producer.produce(data=[m['content'] for m in messages[topic]])

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