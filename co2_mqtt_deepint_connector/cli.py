#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.

import uuid
import typer
from typing import Dict, List, Any

from co2_mqtt_deepint_connector import connect, serve_application_logger


app = typer.Typer()
logger = serve_application_logger()


@app.command()
def run(
    mqtt_broker: str = typer.Argument(default=None, help="MQTT's broker IP")
    , mqtt_port: int = typer.Argument(default=None, help="MQTT's broker port")
    , mqtt_user: str = typer.Argument(default=None, help="MQTT's broker user")
    , mqtt_password: str = typer.Argument(default=None, help="MQTT's broker password")
    , config_url: str = typer.Argument(default=None, help="URL of the mapping (between MQTT and Deep Intelligence) configuration server's endpoint.")
    , deepint_auth_token: str = typer.Argument(default=None, help="Authentication token for AIR Institute")
    , mqtt_client_id: str = typer.Argument(default=None, help="MQTT's client id. If not provided, an UUIDv4 will be generated")
    , mqtt_num_message_limit: int = typer.Argument(default=10, help="number of messages to store before dumpt to AIR Institute. If set to 0 each message is send")
    , quiet_mode_set: bool = typer.Argument(default=False, help=" if set to true no logging information is provided.")) -> None:
    """While running dumps messages received from MQTT into deepint.
    """

    # check arguments
    if mqtt_broker is None \
        or mqtt_port is None \
        or mqtt_user is None \
        or mqtt_password is None \
        or config_url is None \
        or deepint_auth_token is None:
        
        logger.warning(f'ERROR: Any of mqtt_broker({mqtt_broker}), mqtt_user({mqtt_user}), mqtt_password({mqtt_password}), config_url({config_url}) or deepint_auth_token({deepint_auth_token}) not provided.')
        return

    # disable logging if necceary
    if quiet_mode_set:
        logger.disabled = True

    # perform connection
    connect(
        mqtt_broker=mqtt_broker
        , mqtt_port=mqtt_port
        , mqtt_user=mqtt_user
        , mqtt_password=mqtt_password
        , deepint_auth_token=deepint_auth_token
        , config_url=config_url
        , mqtt_client_id=str(uuid.uuid4())
        , mqtt_num_message_limit=mqtt_num_message_limit
    )


def run():
    app()
