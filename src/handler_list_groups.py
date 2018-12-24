import json
from datetime import datetime
import os
import boto3

cognito_client = boto3.client('cognito-idp')

def list_groups(event, context):
    
    if 'UserPoolId' not in os.environ:
        raise KeyError("UserPoolId does not exist in environment variable.")
    
    response = cognito_client.list_groups(
        UserPoolId = os.environ['UserPoolId']
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