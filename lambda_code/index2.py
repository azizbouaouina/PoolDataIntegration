import boto3
import json
import clickhouse_connect
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
    string_data = obj['Body'].read().decode('utf-8')

    lines = string_data.splitlines()

    # Initialize the output list
    output = []
    
    # Process each line
    for line in lines:
    
        # Parse the line as JSON into a dictionary
        data = json.loads(line)
    
        # Extract the required values
        interval = int(data["interval"])
        coreid = data["coreid"]
        # value_time = data['published_at'].split('.')[0]
        
        value_time = datetime.strptime(data['published_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
    
        # Create a row of extracted values
        row = [
            value_time,  # Format time
            coreid,      # Extract coreid
            interval     # Convert interval to integer
        ]
        
        output.append(row)
    
    print(output)


    # Use a ClickHouse Connect client instance to connect to a ClickHouse Cloud service:
    client = clickhouse_connect.get_client(host=host, 
                                            port=8443, 
                                            username=username, 
                                            password=password)
    
    client.command('''CREATE TABLE IF NOT EXISTS fill_the_pool_table(
        time DateTime NOT NULL CODEC(Delta, ZSTD),
        device_id TEXT,
        liters_of_water_filled UInt8,
        ) 
    ENGINE = MergeTree 
    ORDER BY time''')
    
    client.insert('fill_the_pool_table', output, column_names=['time', 'device_id','liters_of_water_filled'])



