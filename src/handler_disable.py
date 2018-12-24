import json
from datetime import datetime
import os
import boto3

cognito_client = boto3.client('cognito-idp')

def disable_user(event, context):
    event = json.loads(event['body'])
    
    if 'UserPoolId' not in os.environ:
        raise KeyError("UserPoolId does not exist in environment variable.")
    if 'Username' not in event:
        raise KeyError("Username does not exist.")
    
    response = cognito_client.admin_disable_user(
        UserPoolId = os.environ['UserPoolId'],
        Username = event['Username']
    )


    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Origin" : "*"
        },
        'body': json.dumps(response, default=support_datetime_default)
    }

def support_datetime_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(repr(obj) + " is not JSON serializable")