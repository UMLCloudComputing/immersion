from immersion_stack import ImmersionStack
import aws_cdk as cdk
import os

app = cdk.App()
ImmersionStack(app, "ImmersionStackDev",
    env = {
        "account": os.getenv('CICD_ACCOUNT_ID'), # Assuming it's only being deployed with GH Actions
        "region": "us-east-1"
    }
)

app.synth()
