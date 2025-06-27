from immersion_stack import ImmersionStack
import aws_cdk as cdk

app = cdk.App()
ImmersionStack(app, "ImmersionStackDev")

app.synth()