import json
import requests
import boto3

s3 = boto3.client('s3')

secret_name_1 = "pool_id"
secret_name_2 = "refresh_token"
region_name = "eu-west-1"

#Set up our Session and Client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

def lambda_handler(event, context):
    
    ###################getting secrets :###################### 
    #secret_1
    # Calling SecretsManager
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name_1
    )
    #Extracting the pool id from the secret
    pool_id = get_secret_value_response['SecretString']

    #secret_2
    # Calling SecretsManager
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name_2
    )
    #Extracting the pool id from the secret
    refresh_token = get_secret_value_response['SecretString']

    ###########################################################
    
    url_prefix = "https://interop.ondilo.com/api/customer/v1"
    
    # Define the parameters
    params = {
    "types[]": "temperature"
    }
    
    data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token,
    "client_id": "customer_api"
    }
    
    # Make the POST request to the token endpoint
    response = requests.post("https://interop.ondilo.com/oauth2/token", data=data)
    
    # Get the new access token from the response
    access_token = response.json()["access_token"]
    
    # Define the headers
    headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/json",
    "Accept-Charset": "utf-8",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Make the GET request to the last measures endpoint
    response = requests.get(url_prefix + "/pools/" + pool_id + "/lastmeasures", params=params, headers=headers)
    
    
    if response.status_code == 200:
            
        data = response.json()
        print(data)
        
        bucket_name = 'ondilo-bucket-aziz'
        file_name = data[0]['value_time'].split('+')[0].replace(":", "-")


        
        uploadByteStream = bytes(json.dumps(data[0]).encode('UTF-8'))
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=uploadByteStream)
        
        print('Put complete')
