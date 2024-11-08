import os
from aws_cdk import (
    Stack,
    aws_apprunner_alpha as apprunner
)
from constructs import Construct

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bot_apprunner = apprunner.Service(self, os.getenv("APP_NAME") + "Service",
                                          apprunner.Source.from_ecr_public(
                                           image_configuration=apprunner.ImageConfiguration(port=8080),
                                           image_identifier="ghcr.io/umlcloudcomputing/immersiondiscordapp:latest"
                                         ))
