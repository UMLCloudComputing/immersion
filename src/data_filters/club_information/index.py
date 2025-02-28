import boto3
import json
import os

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    testMessage = {
        'message': 'hello from lambda'
    }

    sqs.send_message(
        QueueUrl=os.getenv('QUEUE_URL'),
        MessageBody=json.dumps(testMessage)
    )