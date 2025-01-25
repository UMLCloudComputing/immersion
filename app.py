#!/usr/bin/env python3
import os
import aws_cdk as cdk
from immersion.immersion_stack import ImmersionStack


app = cdk.App()
ImmersionStack(app, f'{os.getenv('APP_NAME')}Stack')

app.synth()
