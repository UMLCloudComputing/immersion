import boto3
import json
import requests
import os

# Parse a single organization to extract only important info
def parse_info(item):
    data = {
        "OrgId": item['id'],
        "Name": item['name'],
        "PrimaryContact": item['PrimaryContactId']['campusEmail'],
        "ImageUrl": f"https://se-images.campuslabs.com/clink/images/{item['profilePicture']}",
        "WebsiteKey": f"https://umasslowellclubs.campuslabs.com/engage/organization/{item['websiteKey']}"
    }

    return data

def lambda_handler(event, context):
    # Constants
    api_endpoint = "https://engage-api.campuslabs.com/api/v3.0/organizations/organization?includeCategories=false&includeContactInfo=true&includeSocialMedia=false&isAdminOnly=false&isBranch=false&isShownInPublicDirectory=true"

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
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_endpoint, headers=headers)

        # Process response from API
        data = response.json()
        parsed_data = []
        for item in data['items']:
            parsed_data.append(parse_info(item))
        
        return_data = {
            "Header": "club_information",
            "Body": json.dumps(parsed_data)
        }
        sqs.send_message(
            QueueUrl=os.getenv('QUEUE_URL'),
            MessageBody=json.dumps(return_data)
        )
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
    