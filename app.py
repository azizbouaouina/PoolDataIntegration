#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack_code.ondilo_stack import OndiloStack
from stack_code.fill_the_pool_stack import FillThePoolStack
from stack_code.temperature_stack import TemperatureStack


app = cdk.App()
OndiloStack(app, "OndiloStack")
FillThePoolStack(app,"FillThePoolStack")
TemperatureStack(app,"TemperatureStack")

app.synth()
