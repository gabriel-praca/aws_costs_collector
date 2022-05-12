import json
import os
import s3fs
from datetime import datetime, timedelta
from FetchAWS import FetchAWS
from FetchSnowflake import FetchSnowflake
import pandas as pd
import io

def handler(event, context):

    fs = s3fs.S3FileSystem(use_listings_cache=False)

    def get_output_list(parameters):
        header_result = [["DATE", "TAG", "RESOURCE", "ENVIRONMENT", "AMOUNT", "UNIT"]]
        aws_result = FetchAWS(parameters).fetch()
        snowflake_result = FetchSnowflake(parameters).fetch()

        output = header_result

        if aws_result:
            output += aws_result

        if snowflake_result:
            output += snowflake_result

        return output

    def get_output_csv(result_list, output_delimiter=","):
        output = ""

        for row in result_list:
            first = True

            for col in row:
                if not first:
                    output += output_delimiter + col
                else:
                    output += col

                first = False

            output += "\n"

        return output

    def check_date(parameters, output_delta_days=1, output_date_format="%Y-%m-%d"):
        result_start = parameters['fetch']['start_date']
        result_end = parameters['fetch']['end_date']

        if not result_start:
            parameters['fetch']['start_date'] = (datetime.now() - timedelta(days=output_delta_days)).strftime(output_date_format)

        if not result_end:
            parameters['fetch']['end_date'] = datetime.now().strftime(output_date_format)

    def get_parameters_dict():
        content = ""
        with fs.open(os.getenv('FILE'), 'rb') as f:
            content += f.read().decode("utf-8")

        dict_from_json = json.loads(content)

        return dict_from_json
    
    parameters = get_parameters_dict()
    check_date(parameters)

    output_list = get_output_list(parameters)
    output_csv = get_output_csv(output_list)
    print("\n" + output_csv)

    result_df = pd.read_csv(io.StringIO(output_csv), sep=',')
    
    # Upload the file
    result_df["ENVIRONMENT"].replace({"PROD": "PRD"}, inplace=True)
    result_df.to_csv(os.path.join(os.getenv("OUTPUT_PATH"), datetime.now().strftime('%Y'), "costs_result_" + os.getenv("ENV").lower() + ".csv"), index=False)

    # END
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
