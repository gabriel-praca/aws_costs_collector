# ⚙ Project With Cost Management Engine Job
It is a repository that contains the entire project for cost management engine logic in aws lambda.

Job is responsible for automatically obtaining management costs and making them available on S3.

### (files in config is only for glue jobs configurations DO NOT FORGET CHANGE VALUES IN THE FILES BEFORE EXECUTION!)

## 📝 PREREQUISITES

What is needed before running the script.

Libraries used in this project (included into dockerfile!):

- 📁 Packages
    - 📂 [s3fs](https://pypi.org/project/s3fs/)
    - 📂 [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    - 📂 [pandas](https://pypi.org/project/pandas/)
    - 📂 [snowflake-connector-python](https://pypi.org/project/snowflake-connector-python/)
    - 📂 [awslambdaric](https://pypi.org/project/awslambdaric/)
    - 📂 [cryptography](https://cryptography.io/en/latest/installation/)

## 🔗 JOB ENVIRONMENT VARIABLES (AWS Lambda)

>--SECRET_NAME: Name of the secret with connection informations. 
>
>&emsp; 👉 Example: secret_test
>
>--REGION_NAME: Name of region. 
>
>&emsp; 👉 Example: us-east-1
>
>--ENV: Cost environment to obtain. 
>
>&emsp; 👉 Example: DEV|PRD
>
>--FILE: Parameters file path. 
>
>&emsp; 👉 Example: s3://utils/scripts/parameters.json
>
>--OUTPUT_PATH: Output of csv path. 
>
>&emsp; 👉 Example: s3://utils/costs
>
>--PYTHONIOENCODING: Set default encoding. 
>
>&emsp; 👉 Example: utf8
>
>--SNOW_WAREHOUSE: Warehouse to connect in snowflake. 
>
>&emsp; 👉 Example: DEV_COMMON_MONITORING
>

Parameters like ACCESS_KEY, SECRET_KEY, SNOW_USER and SNOW_PASS is in AWS sercret manager

## 📍 JOB CREATION

To create the job:

1. Copy the project files to a location on your local machine;
2. Change the information you want in the code;
3. Run the below code to build your image:
>docker build -t <*USER_ID*>.dkr.ecr.<*REGION*>.amazonaws.com/<*REPO_IN_ECR*> . 
>
>&emsp; 👉 Example: docker build -t 1234567890.dkr.ecr.us-east-1.amazonaws.com/costs .
4. Run the below code to publish your image on ECR:
>&emsp; docker push <*USER_ID*>.dkr.ecr.<*REGION*>.amazonaws.com/<*REPO_IN_ECR*>
>
>&emsp; 👉 Example: docker push 1234567890.dkr.ecr.us-east-1.amazonaws.com/costs
5. If you get error "no basic auth credentials" to publish image, make sure if your docker config.json has the below informations:
```
{
  "credsStore": "ecr-login"
}
```
6. Create a lambda function with this image as template.
7. Make sure that the lambda function has a sufficient timeout (5 minutes recommended).
8. Make sure that the lambda function has a sufficient memory (512MB recommended).


## 📋 GETTING STARTED

Some examples of configuration files used in this script:

- JSON Parameters Estructure:
```
{
  "fetch": {
    "start_date": "2020-06-01",
    "end_date": ""
  },
  "aws": {
    "enable": true,
    "tag_key": "project",
    "multiply_factor_enable": false,
    "multiply_factor_amount": 1,
    "multiply_factor_unit": "USD"
  },
  "snowflake": {
    "enable": true,
    "account":"<*your-account*>"
    "multiply_factor_enable": true,
    "multiply_factor_amount": 3,
    "multiply_factor_unit": "USD"
  },
  "databricks":{
    "account_id": "",
    "credentials_id": "",
    "storage_configuration_id": ""
  }
}
```

## 🔨 BUILD WITH

* 🐍 [Python](https://www.python.org/downloads/release/python-360/)
* 🐳 [Docker](https://www.docker.com/get-started)
* ☁️ [AWS](https://docs.aws.amazon.com/index.html)

## ✒️ AUTHORS

* **Gabriel Praça** - 💻 *Developer*