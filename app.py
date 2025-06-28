#!/usr/bin/env python3
import os
import aws_cdk as cdk
from immersion.immersion_stack import ImmersionStack


env = cdk.Environment(
    account=os.getenv('AWS_ACCOUNT_ID'), 
    region=os.getenv('AWS_DEFAULT_REGION'))

app = cdk.App()
ImmersionStack(app, f'{os.getenv('APP_NAME')}Stack', env=env)

app.synth()
