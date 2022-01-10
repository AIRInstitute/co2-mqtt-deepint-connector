#!usr/bin/python

# Copyright 2021 AIR Institute
# See LICENSE for details.


import deepint
import pandas as pd
import Crypto.Cipher.AES
from Crypto.Cipher import AES
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

    def __init__(self, auth_token: str, organization_id: str, workspace_id: str, source_id: str, cipher_key: str = None) -> None:
        self.source_id = source_id
        self.workspace_id = workspace_id
        self.organization_id = organization_id
        self.credentials = deepint.Credentials.build(token=auth_token)

        self.cipher_key = cipher_key

    def produce(self, data: List[str]) -> None:
        """Produces the given data to AIR Institute
        
        Args:
            data: JSON formatted data to dump into AIR Institute.
        """
        try:

            if cipher_key is not None:
                decipher = AES.new(self.cipher_key,AES.MODE_CBC,IV)
                data = [decipher.decrypt(d) for d in data]

            data = [json.loads(d) for d in data]

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
            logger.info(f"publishing {len(df)} messages to source {self.source_id}")
            source.instances.update(data=df, replace=False)
            t.resolve()

        except Exception as e:
            logger.warning(f'Exception during Deep Intelligence source update {e}')
