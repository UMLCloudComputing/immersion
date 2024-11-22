#!/usr/bin/env python3
import os

import aws_cdk as cdk

from immersion.immersion_stack import ImmersionStack

from dotenv import load_dotenv

load_dotenv()

app = cdk.App()
ImmersionStack(app, "ImmersionStack", 
               env=cdk.Environment(account=os.getenv('AWS_ACCOUNT_ID'), region=os.getenv('AWS_DEFAULT_REGION')),
)

app.synth()
