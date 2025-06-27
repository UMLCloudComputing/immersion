from aws_cdk import (
    # Duration,
    Stack,
    Duration,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_sqs as sqs,
    aws_cloudwatch as cw,
    aws_applicationautoscaling as appautoscaling,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as lambda_python,
    aws_ssm as ssm
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
from aws_cdk.aws_cloudwatch_actions import ApplicationScalingAction
from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table Definitions
        serverTable = dynamodb.TableV2(
            self, 
            f"{os.getenv('APP_NAME')}ServerTable",
            partition_key=dynamodb.Attribute(name='serverId', type=dynamodb.AttributeType.STRING),
        )

        onboardingTable = dynamodb.TableV2(
            self,
            f"{os.getenv('APP_NAME')}OrganizationTable",
            partition_key=dynamodb.Attribute(name='organizationId', type=dynamodb.AttributeType.NUMBER)
        )

        cacheTable = dynamodb.TableV2(
            self,
            f"{os.getenv('APP_NAME')}APICacheTable",
            partition_key=dynamodb.Attribute(name='clubId', type=dynamodb.AttributeType.STRING),
        )

        eventTable = dynamodb.TableV2(
            self,
            f"{os.getenv('APP_NAME')}EventTable",
            partition_key=dynamodb.Attribute(name='eventId', type=dynamodb.AttributeType.STRING),
        )

        # SQS Queue and Size Metric Defintion
        queue = sqs.Queue(
            self,
            f"{os.getenv('APP_NAME')}DataQueue",
            queue_name=f'{os.getenv('APP_NAME')}_Data_Queue',
        )

        scale_metric = queue.metric_approximate_number_of_messages_visible(
            period=Duration.minutes(1),
            statistic="Average",
        )

        scale_out_alarm = scale_metric.create_alarm(
            self,
            f"{os.getenv('APP_NAME')}DataParserScaleOutAlarm",
            alarm_name=f'{os.getenv('APP_NAME')}DataProcessScaleOutAlarm',
            threshold=1, 
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=cw.TreatMissingData.NOT_BREACHING
        )

        scale_in_alarm = scale_metric.create_alarm(
            self,
            f"{os.getenv('APP_NAME')}DataParserScaleInAlarm",
            alarm_name=f'{os.getenv('APP_NAME')}DataParserScaleInAlarm',
            threshold=0,
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=cw.TreatMissingData.NOT_BREACHING
        )

        # Container Cluster Component Defintion
        vpc = ec2.Vpc.from_lookup(
            self,
            'VPC',
            vpc_name='Club-VPC'
        )

        cluster = ecs.Cluster(
            self,
            f"{os.getenv('APP_NAME')}ServiceCluster",
            vpc=vpc
        )

        # Discord App Container Definition 
        app_task_defintion = ecs.FargateTaskDefinition(
            self,
            f"{os.getenv('APP_NAME')}DiscordAppTaskDefinition",
            memory_limit_mib=1024, # 1 GB
            cpu=512, # 0.5 vCPU
        )

        app_task_defintion.add_container(
            f"{os.getenv('APP_NAME')}DiscordApp",
            image=ecs.ContainerImage.from_docker_image_asset(
                DockerImageAsset(
                    self,
                    f"{os.getenv('APP_NAME')}DiscordAppDockerImage",
                    directory='src/discordapp/'
                )
            ),
            environment={
                'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN')
            }
        )

        app_service = ecs.FargateService(
            self,
            f"{os.getenv('APP_NAME')}DiscordAppService",
            cluster=cluster,
            task_definition=app_task_defintion,
            assign_public_ip=True
        )
        
        parser_logging = ecs.AwsLogDriver(
            stream_prefix='parserlogs'
        )

        # Data Parser Task Definition
        parser_task_definition = ecs.FargateTaskDefinition(
            self,
            f"{os.getenv('APP_NAME')}DataParserTask",
            memory_limit_mib=1024, # 1 GB
            cpu=512, # 0.5 vCPU
        )

        parser_task_definition.add_container(
            f"{os.getenv('APP_NAME')}DataParser",
            # TODO: REFACTOR TO USE GITHUB CONTAINER REGISTRY!
            image=ecs.ContainerImage.from_docker_image_asset( 
                DockerImageAsset(
                    self,
                    f"{os.getenv('APP_NAME')}DataParserImage",
                    directory='src/data_parser/',
                )
            ),
            environment={
                'QUEUE_URL': queue.queue_url,
                'ORGANIZATION_TABLE': onboardingTable.table_name,
            },
            logging=parser_logging,
        )
        queue.grant_consume_messages(parser_task_definition.task_role)
        onboardingTable.grant_write_data(parser_task_definition.task_role)

        parser_service = ecs.FargateService(
            self,
            f"{os.getenv('APP_NAME')}DataParserService",
            cluster=cluster,
            task_definition=parser_task_definition,
            assign_public_ip=True
        )

        # Scale metrics for data parser service
        scaling_target = appautoscaling.ScalableTarget(
            self,
            id=f"{os.getenv('APP_NAME')}ParserScalingTarget",
            service_namespace=appautoscaling.ServiceNamespace.ECS,
            scalable_dimension='ecs:service:DesiredCount',
            min_capacity=0,
            max_capacity=1,
            resource_id=f'service/{parser_service.cluster.cluster_name}/{parser_service.service_name}'
        )

        scale_out_action = appautoscaling.StepScalingAction(
            self,
            'ParserScaleOutAction',
            scaling_target=scaling_target,
            adjustment_type=appautoscaling.AdjustmentType.EXACT_CAPACITY,
        )

        scale_out_action.add_adjustment(
            adjustment=1,
            lower_bound=0
        )

        
        scale_out_action.add_adjustment(
            adjustment=0,
            upper_bound=0
        )

        scale_out_alarm.add_alarm_action(ApplicationScalingAction(scale_out_action))

        scale_in_action = appautoscaling.StepScalingAction(
            self,
            'ParserScaleInAction',
            scaling_target=scaling_target,
            adjustment_type=appautoscaling.AdjustmentType.EXACT_CAPACITY,
        )

        scale_in_action.add_adjustment(
            adjustment=0,
            lower_bound=0,
        )

        scale_in_action.add_adjustment(
            adjustment=1,
            upper_bound=0,
        )

        scale_in_alarm.add_alarm_action(ApplicationScalingAction(scale_in_action))

        # TODO: figure out how to make a layer for python dependencies
        # filter_layer = _lambda.LayerVersion(
        #     self,
        #     f'{os.getenv('APP_NAME')}FilterLayer',
            
        # )

        # Data Filter Lambda Functions
        engage_api_key_param = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            f"{os.getenv('APP_NAME')}APIKEY",
            parameter_name=f"{os.getenv('SSM_PARAMETER_NAME_API')}"
        )
        
        club_information_lambda = lambda_python.PythonFunction(
            self,
            f"{os.getenv('APP_NAME')}ClubInformationLambda",
            runtime=Runtime.PYTHON_3_13,
            entry='src/data_filters/onboarding',
            handler='lambda_handler',
            environment={
                'QUEUE_URL': queue.queue_url
            },
        )
        queue.grant_send_messages(club_information_lambda)
        engage_api_key_param.grant_read(club_information_lambda)