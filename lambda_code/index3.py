import requests
import json
from datetime import datetime
import boto3
import pytz

# Create an S3 client object
s3_client = boto3.client('s3')

# Your secret's name and region
region_name = "eu-west-1"

#Set up our Session and Client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)


def lambda_handler(event, context):
    
    ###################getting secret :###################### 
    #secret_1
    # Calling SecretsManager
    get_secret_value_response = client.get_secret_value(
        SecretId='api_key'
    )
    #Extracting the api-key from the secret
    api_key = get_secret_value_response['SecretString']
    ##########################################################

    # Specify the time zone for France
    france_timezone = pytz.timezone('Europe/Paris')

    # Get the current time in France
    france_time = datetime.now(france_timezone)

    formatted_time = france_time.strftime("%Y-%m-%d %H:00:00")

    print(formatted_time)


    # Define the start and end dates for the weather data retrieval
    start_date = formatted_time
    end_date = formatted_time

    # Set the latitude and longitude coordinates for the weather data retrieval
    latitude = 44.7849824
    longitude = -0.7008536

    # Send a GET request to the weather API to retrieve the data
    r = requests.get('https://api.oikolab.com/weather',
                    params={'param': ['temperature','wind_speed','wind_direction','relative_humidity','total_cloud_cover','total_precipitation'],
                            'start': start_date,
                            'end': end_date,
                            'lat': latitude,
                            'lon': longitude,
                            'api-key': api_key}
                    )

    # Parse the JSON response from the API into a Python dictionary
    weather_data = json.loads(r.json()['data'])
    weather_data['data']= weather_data['data'][0]

    # Define the columns to be included in the filtered data
    columns_filtered = ['time','latitude','longitude','temperature','wind_speed','wind_direction','relative_humidity','total_cloud_cover','total_precipitation']

    # Filter and transform the weather data to the desired format
    data_filtered = [[formatted_time] + [float(x) for x in weather_data['data'][:1][0].strip('()').split(', ')] + weather_data['data'][4:]]
    data_filtered=data_filtered[0]
    
    file_name = formatted_time.replace(":", "-").replace(' ','T')

    res = {}
    for key in columns_filtered:
        for value in data_filtered:
            res[key] = value
            data_filtered.remove(value)
            break
    

    bucket_name = 'temperature-bucket-aziz'
    
    
    uploadByteStream = bytes(json.dumps(res).encode('UTF-8'))
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=uploadByteStream)
    
    print('Put complete')