from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb
)
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()

class ImmersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        serverTable = dynamodb.TableV2(
            self, 
            f'{os.getenv('APP_NAME')}ServerTable',
            partition_key=dynamodb.Attribute(name='serverId', type=dynamodb.AttributeType.STRING)
        )

        cacheTable = dynamodb.TableV2(
            self,
            f'{os.getenv('APP_NAME')}APICacheTable',
            partition_key=dynamodb.Attribute(name='clubId', type=dynamodb.AttributeType.STRING)
        )

        eventTable = dynamodb.TableV2(
            self,
            f'{os.getenv('APP_NAME')}EventTable',
            partition_key=dynamodb.Attribute(name='eventId', type=dynamodb.AttributeType.STRING)
        )