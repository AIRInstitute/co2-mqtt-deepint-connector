#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import requests
from typing import Dict, List, Any, Optional

from co2_mqtt_deepint_connector import DeepintProducer, serve_application_logger


logger = serve_application_logger()


class MessageRouter:
    """Builds :obj:`co2_mqtt_deepint_connector.deepint_producer.DeepintProducer` for a MQTT topic.

    Attributes:
        router: the configuration used to route between MQTT topic and Deep Intelligence source.
        config_url: the URL of the endpoint used to fetch the mapping (between MQTT and Deep Intelligence) configuration.
        deepint_auth_token: token to auth against Deep Intelligence and perform operations.

    Args:
        config_url: the URL of the endpoint used to fetch the mapping (between MQTT and Deep Intelligence) connector.
        deepint_auth_token: token to auth against Deep Intelligence and perform operations.
    """

    def __init__(self, config_url: str, deepint_auth_token:str) -> None:
        self.router = {}
        self.config_url = config_url
        self.deepint_auth_token = deepint_auth_token

    def update(self, mqtt_topic: str) -> None:
        """ Updates the configuration checking the API.
        """

        try:
            response = requests.get(url=self.config_url, params={'topic': mqtt_topic})

            if response.status_code != 200:
                logger.warning(f'API response returned code {response.status_code} with message: {response.json()}')
                return

            response_info = response.json()

            if response_info is not None:
                topic_info = {
                    'token': response_info['token'],
                    'source_id': response_info['srcId'],
                    'workspace_id': response_info['wsId'],
                    'organization_id': response_info['orgId']
                }

                self.router[mqtt_topic] = topic_info

        except Exception as e:
            logger.warning(f'Exception on config fetch {e}')

    def resolve(self, mqtt_topic:str) -> Optional[DeepintProducer]:
        """Builds a Deep Intelligence Producer for a given MQTT topic.
        
        If the topic is not stored into internal configuration, the configuration is updated.

        Args:
            mqtt_topic: topic where the information is taken from

        Returns:
            A producer to Deep Intelligence in the case of finging the topic in the internal router configuration. Else return None.
        """

        # if the topic is not in the router update the configuration
        if mqtt_topic not in self.router:
            self.update(mqtt_topic)

        # if the topic is not in router after updating the config finish
        if mqtt_topic not in self.router:
            return None

        # retrieve the configuration from router
        token = self.router[mqtt_topic]['token']
        source_id = self.router[mqtt_topic]['source_id']
        workspace_id = self.router[mqtt_topic]['workspace_id']
        organization_id = self.router[mqtt_topic]['organization_id']

        # build producer
        producer = DeepintProducer(auth_token=self.deepint_auth_token
                , organization_id=organization_id
                , workspace_id=workspace_id
                , source_id=source_id
                , cipher_key=token
            )

        return producer
