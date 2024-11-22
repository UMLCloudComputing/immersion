import os
from aws_cdk import (
    Stack,
    aws_apprunner_alpha as apprunner,
    aws_secretsmanager as secretsmanager,
    aws_ssm as ssm,
)
from constructs import Construct

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        parameter = ssm.StringParameter.from_string_parameter_name(
            self, 
            f'SSMParameter{construct_id}',
            string_parameter_name=os.getenv('SSM_PARAMETER_NAME')
        )
        bot_apprunner = apprunner.Service(
            self, 
            os.getenv("APP_NAME") + "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(
                    port=8080, environment_secrets={
                    "DISCORD_TOKEN": apprunner.Secret.from_ssm_parameter(parameter),
                    }
                ),
                image_identifier="public.ecr.aws/k4n1q0u7/immersion/discordapp:latest"
            )
        )
