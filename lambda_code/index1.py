import clickhouse_connect
import boto3
import json
from datetime import datetime

# Create an S3 client object
s3_client = boto3.client('s3')

# Your secret's name and region
secret_name = "clickhouse_credentials"
region_name = "eu-west-1"

def lambda_handler(event, context):

    #Set up our Session and Client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # Extract clickhouse credentials from the secret 
    # Calling SecretsManager
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    #Extracting the key/value from the secret
    secret = get_secret_value_response['SecretString']

    # Parse the string as JSON
    secret_dict = json.loads(secret)

    host = secret_dict["host"]
    username = secret_dict["username"]
    password = secret_dict["password"]

    # Extract the name of the S3 bucket and the file name from the event object
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    print(bucket_name)
    print(file_name)
    # Get the file data from S3 using the S3 client object
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    
    # read the file
    data = json.loads(obj['Body'].read().decode('utf-8'))
    
        
    if data['is_valid'] == True :
            
        time = datetime.strptime(data['value_time'], '%Y-%m-%dT%H:%M:%S%z')
        temperature_value = float(data['value'])
        
        row = [[time,temperature_value]]
        
        
        # Use a ClickHouse Connect client instance to connect to a ClickHouse Cloud service:
        client = clickhouse_connect.get_client(host=host, 
                                                port=8443, 
                                                username=username, 
                                                password=password)
        
        client.command('''CREATE TABLE IF NOT EXISTS ondilo_table(
            time DateTime NOT NULL CODEC(Delta, ZSTD),
            temperature Float32 CODEC(Delta, ZSTD),
            ) 
        ENGINE = MergeTree 
        ORDER BY time''')
        
        client.insert('ondilo_table', row, column_names=['time', 'temperature'])