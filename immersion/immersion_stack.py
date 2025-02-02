from aws_cdk import (
    # Duration,
    Stack,
    aws_autoscaling as autoscaling,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecsp,
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Container Cluster Component Defintion
        vpc = ec2.Vpc(
            self,
            f'{os.getenv('APP_NAME')}VPC',
        )

        cluster = ecs.Cluster(
            self,
            f'{os.getenv('APP_NAME')}ServiceCluster',
            vpc=vpc
        )

        app_task_defintion = ecs.FargateTaskDefinition(
            self,
            f'{os.getenv('APP_NAME')}DiscordAppTaskDefinition',
            memory_limit_mib=1024, # 1 GB
            cpu=512, # 0.5 vCPU
        )

        app_task_defintion.add_container(
            f'{os.getenv('APP_NAME')}DiscordApp', 
            image=ecs.ContainerImage.from_docker_image_asset(
                DockerImageAsset(
                    self,
                    f'{os.getenv('APP_NAME')}DiscordAppDockerImage',
                    directory='src/discordapp/'
                )
            ),
            environment={
                'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN')
            }
        )

        app_service = ecs.FargateService(
            self,
            f'{os.getenv('APP_NAME')}DiscordAppService',
            cluster=cluster,
            task_definition=app_task_defintion
        )

        # DynamoDB Table Definitions
        serverTable = dynamodb.TableV2(
            self, 
            f'{os.getenv('APP_NAME')}ServerTable',
            partition_key=dynamodb.Attribute(name='serverId', type=dynamodb.AttributeType.STRING),
            deletion_protection=True
        )

        cacheTable = dynamodb.TableV2(
            self,
            f'{os.getenv('APP_NAME')}APICacheTable',
            partition_key=dynamodb.Attribute(name='clubId', type=dynamodb.AttributeType.STRING),
            deletion_protection=True
        )

        eventTable = dynamodb.TableV2(
            self,
            f'{os.getenv('APP_NAME')}EventTable',
            partition_key=dynamodb.Attribute(name='eventId', type=dynamodb.AttributeType.STRING),
            deletion_protection=True
        )