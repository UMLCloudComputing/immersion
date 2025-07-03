from immersion_stack import ImmersionStack
import aws_cdk as cdk
from dotenv import load_dotenv
import os

app = cdk.App()

load_dotenv()

ImmersionStack(app, "ImmersionStackDev",
    env = {
        "account": os.getenv('CICD_ACCOUNT_ID'), # Assuming it's only being deployed with GH Actions
        "region": "us-east-1"
    }
)

app.synth()
