import os
import requests
from FetchABC import FetchABC


###
### WIP / TODO
###

class FetchDatabricks(FetchABC):
    def __init__(self):
        self.account_id = ('DATABRICKS_ACCOUNT_ID')
        self.credentials_id = os.getenv('DATABRICKS_CREDENTIALS_ID')
        self.storage_configuration_id = os.getenv('DATABRICKS_STORAGE_CONFIG_ID')
        self.url = 'https://accounts.cloud.databricks.com/api/2.0/accounts/' + self.account_id + '/log-delivery'

    def fetch(self, start, end):
        request_body = {
            "log_delivery_configuration": {
                "log_type": "BILLABLE_USAGE",
                "config_name": "billable usage config",
                "output_format": "CSV",
                "delivery_path_prefix": "usage-data",
                "credentials_id": self.credentials_id,
                "storage_configuration_id": self.storage_configuration_id,
                "delivery_start_time": start,
                "workspace_ids_filter": [
                    1234567890,
                    1234567890
                ]
            }
        }

        result = self.parse(request_body)

        return result

    def parse(self, request_body):
        return requests.post(self.url, body=request_body)

    def get_connection(self):
        pass
