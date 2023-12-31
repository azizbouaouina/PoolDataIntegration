
# Data integration into Clickhouse using AWS services and Python

This repository utilizes Infrastructure as Code to create essential AWS stacks for securely and automatically integrating pool related data from multiple sources into ClickHouse Cloud.

## Table of Contents
- [Requirements](#requirements)
- [Functionality](#functionality)
- [Installation and Deployment](#installation-and-deployment)

## Requirements

- [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/fr/cdk/)
- [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/fr/cli/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pypi.org/project/pip/)

## Functionality

![7](https://github.com/azizbouaouina/PoolDataIntegration/assets/104959387/a827312b-6ca2-4b3c-adc6-c177be56de9a)

The first stack involves the integration of pool fillage data from an S3 bucket located in a different AWS account into Clickhouse Cloud whenever new data becomes available.

The second stack involves saving hourly weather data for the pool's location in an S3 bucket and subsequently integrating this data into Clickhouse Cloud.

The third stack involves saving hourly pool temperature data in an S3 bucket and subsequently integrating this data into Clickhouse Cloud.

## Installation and Deployment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

To run this project locally, follow these steps:

Clone the repository :

```
git clone https://github.com/azizbouaouina/PoolDataIntegration
```

Create a virtualenv :

```
python -m venv .venv
```

Use the following step to activate your virtualenv :

If tou are on MacOS and Linux

```
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
.venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

And finally deploy the stack to your default AWS account.

```
cdk deploy
```


Enjoy!
