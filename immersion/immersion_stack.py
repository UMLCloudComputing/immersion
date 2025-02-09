from aws_cdk import (
    # Duration,
    Stack,
    Duration,
    aws_autoscaling as autoscaling,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_sqs as sqs,
    aws_cloudwatch as cw,
    aws_autoscaling as autoscaling
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SQS Queue and Size Metric Defintion
        queue = sqs.Queue(
            self,
            f'{os.getenv('APP_NAME')}DataQueue',
            queue_name=f'{os.getenv('APP_NAME')}_Data_Queue'
        )

        scale_metric = queue.metric_approximate_number_of_messages_visible(
            period=Duration.minutes(5),
            statistic="Average"
        )

        scale_out_alarm = scale_metric.create_alarm(
            self,
            f'{os.getenv('APP_NAME')}DataProcessScaleOutAlarm',
            alarm_name=f'{os.getenv('APP_NAME')}DataProcessScaleOutAlarm',
            threshold=0,
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            treat_missing_data=cw.TreatMissingData.NOT_BREACHING
        )

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

        # Discord App Container Definition 
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

        # Data Parser Task Definition
        parser_service = ecs_patterns.QueueProcessingFargateService(
            self,
            f'{os.getenv('APP_NAME')}DataParserService',
            memory_limit_mib=1024, # 1 GB
            cpu=512, # 0.5 vCPU
            # TODO: REFACTOR TO USE GITHUB CONTAINER REGISTRY!!!
            image=ecs.ContainerImage.from_docker_image_asset( 
                DockerImageAsset(
                    self,
                    f'{os.getenv('APP_NAME')}DataParserImage',
                    directory='src/data_parser/'
                )
            ),
            min_scaling_capacity=0,
            max_scaling_capacity=1,
            cluster=cluster,
            queue=queue,
            scaling_steps=[ # NEEDS TO BE PLAYED AROUND WITH
                {'upper': 0, 'change': -1},
                {'lower': 1, 'change': 1},
            ],
            cooldown=Duration.seconds(5) # TODO: ADJUST
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