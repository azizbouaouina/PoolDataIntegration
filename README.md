
# Data integration into Clickhouse using AWS services and Python

This repository utilizes Infrastructure as Code to create essential AWS stacks for securely and automatically integrating pool related data from multiple sources into ClickHouse Cloud.

## Table of Contents
- [Requirements](#requirements)
- [Functionality](#functionality)
- [Installation and Deployment](#installationanddeployment)

## Requirements

- [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/fr/cdk/)
- [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/fr/cli/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pypi.org/project/pip/)

## Functionality



## Installation and Deployment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

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
