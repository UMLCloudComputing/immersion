from immersion_stack import ImmersionStack
import aws_cdk as cdk

app = cdk.App()
ImmersionStack(app, "ImmersionStackDev", {
    "env": {
        "account": "default",
        "region": "us-east-1"
    }
})

app.synth()
