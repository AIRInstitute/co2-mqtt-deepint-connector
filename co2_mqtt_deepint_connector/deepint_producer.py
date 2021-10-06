#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import deepint
import pandas as pd
from typing import Dict, List, Any

from co2_mqtt_deepint_connector import serve_application_logger


logger = serve_application_logger()


class DeepintProducer:
    """Produces to AIR Institute the given data, updating a source.

    Attributes:
        conn: connection to a deepint.net source.

    Args:
        auth_token: Authentication token for AIR Institute.
        organization_id: Deep intelligence organization's id, where source is located.
        workspace_id: Deep intelligence workspace's id, where source is located.
        source_id: Deep intelligence source's id, where data will be dumped.
    """

    def __init__(self, auth_token: str, organization_id: str, workspace_id: str, source_id: str) -> None:
        self.source_id = source_id
        self.workspace_id = workspace_id
        self.organization_id = organization_id
        self.credentials = deepint.Credentials.build(token=auth_token)

    def produce(self, data: List[Dict[str, Any]]) -> None:
        """Produces the given data to AIR Institute
        
        Args:
            data: JSON formatted data to dump into AIR Institute.
        """
        try:

            # build dataframe with data
            df = pd.DataFrame(data=data)

            # build source
            source = deepint.Source.build(
                        credentials=self.credentials
                        ,organization_id=self.organization_id
                        ,workspace_id=self.workspace_id
                        ,source_id=self.source_id
                    )

            # create dataframe and send it to deep intelligence
            logger.info(f"publishing message {data}")
            source.instances.update(data=df, replace=False)
        except Exception as e:
            logger.info(e)

