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

    # parse the file as a JSON
    data = json.loads(string_data)

    # Extract the required values

    latitude = data['latitude']
    longitude = data['longitude']
    humidity = data['relative_humidity']
    temperature = data['temperature']
    time = value_time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
    total_cloud_cover = data['total_cloud_cover']
    total_precipitation = data['total_precipitation']
    wind_direction = data['wind_direction']
    wind_speed = data['wind_speed']

    # Initialize the output list
    output = [[time,latitude,longitude,temperature,wind_speed,wind_direction,humidity,total_cloud_cover,total_precipitation]]
        
    print(output)

    # Use a ClickHouse Connect client instance to connect to a ClickHouse Cloud service:
    client = clickhouse_connect.get_client(host=host, 
                                            port=8443, 
                                            username=username, 
                                            password=password)
    
    client.command('''CREATE TABLE IF NOT EXISTS weather_table(
        time DateTime NOT NULL CODEC(Delta, ZSTD),
        latitude Float32,
        longitude Float32,
        temperature Float32 CODEC(Delta, ZSTD),
        wind_speed Float32 CODEC(Delta, ZSTD),
        wind_direction Float32 CODEC(Delta, ZSTD),
        relative_humidity Float32 CODEC(Delta, ZSTD),
        total_cloud_cover Float32 CODEC(Delta, ZSTD),
        total_precipitation Float32 CODEC(Delta, ZSTD),        
        ) 
    ENGINE = MergeTree 
    ORDER BY time''')
    
    client.insert('weather_table', output, column_names=['time', 'latitude','longitude','temperature','wind_speed',
                                                         'wind_direction','relative_humidity','total_cloud_cover','total_precipitation'])

