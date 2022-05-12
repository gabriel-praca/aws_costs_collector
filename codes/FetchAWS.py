import boto3
import base64
import json
from FetchABC import FetchABC
from decimal import *
import os


class FetchAWS(FetchABC):
    def __init__(self, parameters):
        self.environment = os.getenv("ENV")
        self.start_date = parameters["fetch"]["start_date"]
        self.end_date = parameters["fetch"]["end_date"]

        self.enable = parameters["aws"]["enable"]
        # self.access_key = os.getenv("ACCESS_KEY")
        # self.secret_key = os.getenv("SECRET_KEY")
        
        self.secret = self.getSecret()
        self.tag_key = parameters['aws']['tag_key']

        self.multiply_factor = parameters["aws"]["multiply_factor_enable"]
        self.amount_factor = parameters["aws"]["multiply_factor_amount"]
        self.amount_unit = parameters["aws"]["multiply_factor_unit"]

    def fetch(self):
        if self.enable:
            print("FETCHING AWS...")
        else:
            print("SKIPPING AWS...")
            return

        response = self.get_connection().get_cost_and_usage(
            Metrics=['BlendedCost'],
            Granularity='DAILY',
            TimePeriod={
                'Start': self.start_date,
                'End': self.end_date
            },
            GroupBy=[
                  {
                      'Type': 'TAG',
                      'Key': self.tag_key
                  },
                  {
                      'Type': 'DIMENSION',
                      'Key': 'SERVICE'
                  },
            ],
        )
        result = self.parse(response["ResultsByTime"])

        return result

    def parse(self, json_result):
        result = []

        for item in json_result:
            if len(item["Groups"]) == 0:
                continue

            for group in item["Groups"]:
                amount = group["Metrics"]["BlendedCost"]["Amount"]
                result.append(
                    [
                        item["TimePeriod"]["Start"],
                        group["Keys"][0].replace(self.tag_key + "$", "").upper(),
                        group["Keys"][1].upper().replace("AMAZON", "AWS"),
                        self.environment,
                        str(Decimal(amount) * self.amount_factor) if self.multiply_factor else amount,
                        self.amount_unit if self.multiply_factor else group["Metrics"]["BlendedCost"]["Unit"]
                    ]
                )

        return result

    def getSecret(self):
        secret_name = os.getenv("SECRET_NAME")
        region_name = os.getenv("REGION_NAME")

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)

            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return json.loads(secret)
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return json.loads(decoded_binary_secret)

        except Exception as e:
            raise e

    def get_connection(self):
        if self.secret["ACCESS_KEY"] and self.secret["SECRET_KEY"]:
            return boto3.client('ce', aws_access_key_id=self.secret["ACCESS_KEY"], aws_secret_access_key=self.secret["SECRET_KEY"])

        return boto3.client('ce')
