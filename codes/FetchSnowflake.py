import os
import boto3
import base64
import json
import snowflake.connector
from FetchABC import FetchABC
import os


class FetchSnowflake(FetchABC):
    def __init__(self, parameters):

        self.environment = os.getenv("ENV") if os.getenv("ENV").upper() == 'DEV' else 'PROD'
        self.start_date = parameters["fetch"]["start_date"]
        self.end_date = parameters["fetch"]["end_date"]

        self.enable = parameters["snowflake"]["enable"]
        # self.user = os.getenv("SNOW_USER")
        # self.password = os.getenv("SNOW_PASS")
        
        self.secret = self.getSecret()
        self.warehouse = os.getenv("SNOW_WAREHOUSE")
        self.account = parameters["snowflake"]["account"]

        self.multiply_factor = parameters["snowflake"]["multiply_factor_enable"]
        self.amount_factor = parameters["snowflake"]["multiply_factor_amount"]
        self.amount_unit = parameters["snowflake"]["multiply_factor_unit"]

        self.database = "SNOWFLAKE"
        self.schema = "ACCOUNT_USAGE"
        self.table = "METERING_HISTORY"
        self.columns = [
           "split_part(start_time, ' ', 0) as DATE",
           "split_part(name, '_', 3) as BUSINESS_NOTE",
          #  "split_part(name, '_', 2) as PROJECT",
           "concat('SNOWFLAKE_', split_part(service_type, '_', 0), '_', split_part(name, '_', -1)) as RESOURCE",
           "split_part(name, '_', 0) as ENVIRONMENT",
           "sum(credits_used) * " + str(self.amount_factor) + " as AMOUNT" if self.multiply_factor else "sum(credits_used) as AMOUNT",
           "'" + self.amount_unit + "' as UNIT" if self.multiply_factor else "'CREDIT' as UNIT",
       ]

        self.group_by = ["name", "date", "service_type"]
        self.order_by = ["date"]

    def fetch(self):
        if self.enable:
            print("FETCHING SNOWFLAKE...")
        else:
            print("SKIPPING SNOWFLAKE...")
            return

        conditions = "start_time between '" + self.start_date + "' and ' " + self.end_date + " ' and ENVIRONMENT = '" + self.environment + "'"

        sql_command = "select " \
                      + ', '.join(self.columns) \
                      + " from " + self.schema + "." + self.table \
                      + " where " + conditions\
                      + " group by " + ','.join(self.group_by) \
                      + " order by " + ", ".join(self.order_by)

        con = self.get_connection()
        
        cursor = con.cursor().execute(sql_command)

        result = self.parse(cursor)

        con.close()

        return result

    def parse(self, cursor):
        result = []
        for row in cursor:
            line = []

            for col in row:
                line.append(str(col))

            result.append(line)

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
        con = snowflake.connector.connect(
            user=self.secret["SNOW_USER"],
            password=self.secret["SNOW_PASS"],
            account=self.account,
            warehouse=self.warehouse,
            database=self.database
        )

        return con
