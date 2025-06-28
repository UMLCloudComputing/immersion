import boto3
import json
import requests
import os

# Parse a single organization to extract only important info
def parse_info(item, numMembers):
    return {
        "OrgId": item['id'],
        "Name": item['name'],
        "PrimaryContact": item['primaryContactId']['campusEmail'],
        "ImageUrl": f"https://se-images.campuslabs.com/clink/images/{item['profilePicture']}",
        "WebsiteKey": f"https://umasslowellclubs.campuslabs.com/engage/organization/{item['websiteKey']}",
        "NumMembers": numMembers,
        "settings": json.dumps({}),
    }


# Similar to onboard variant, provides more info into table
def lambda_handler(event, context):
    # Constants
    api_endpoint_main = f"https://engage-api.campuslabs.com/api/v3.0/organizations/organization?includeCategories=false&includeContactInfo=true&includeSocialMedia=false&isAdminOnly=false&isBranch=false&isShownInPublicDirectory=true&id={event["body"]["id"]}"
    api_endpoint_member_count = f"https://engage-api.campuslabs.com/api/v3.0/organizations/organization/{event["body"]["id"]}/roster"

    # Service configuration
    sqs = boto3.client('sqs')
    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(
        Name="engage_api_key_test",
        WithDecryption=True
    )

    # Define headers with API key
    api_key = response['Parameter']['Value']
    headers = {
        'X-Engage-Api-Key': api_key,
        'accept': 'application/json'
    }

    try:
        # Try both
        # Get primary club data
        response_main = requests.get(api_endpoint_main, headers=headers)
        # Get member count for club in seperate API call
        response_member_count = requests.get(api_endpoint_member_count, headers=headers)

        # Process response from API
        data_main = response_main.json()
        member_count = float(response_member_count.json()['totalItems'])
        
        return_data = {
            "Header": "club_information",
            "Body": [parse_info(data_main['items'][0], member_count)]
        }

        sqs.send_message(
            QueueUrl=f'{os.getenv('QUEUE_URL')}',
            MessageBody=json.dumps(return_data)
        )
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
    